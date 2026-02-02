import pandas as pd
import numpy as np
from funcionsAuxiliars import *

# --- CONFIGURACIÓ ---
INPUT_CONTAINER = "02-silver"
INPUT_FILE = "feb_silver_dataset.csv"
OUTPUT_CONTAINER = "03-gold"
OUTPUT_FILE = "feb_gold_dataset.csv"

# FUNCIONS DE NETEJA I PREPARACIÓ
def clean_minutes(df):
    """Converteix segons a minuts si cal."""
    if df['minutes'].mean() > 1000:
        print("Corregint unitats de temps (Segons -> Minuts)...")
        df['minutes'] = df['minutes'] / 60
    return df

def normalize_per_40(df):
    """Projecta les estadístiques de volum a 40 minuts."""
    print("Normalitzant estadístiques (Per 40 min)...")
    stats_cols = [
        # Anotació i Volum de Tir
        'pts', 
        'fga', '2pa', '3pa', 'fta',
        
        # Rebots
        'orb', 'drb', 'trb',
        
        # Playmaking i Defensa
        'ast', 'stl', 'blk', 'tov', 
        
        # Faltes
        'pf', 'pfd'
    ]
    for col in stats_cols:
        if col in df.columns:
            df[f'{col}_p40'] = np.where(df['minutes'] > 0, (df[col] / df['minutes']) * 40, 0)
    return df

# FUNCIONS DE CÀLCUL AVANÇAT
def calc_efficiency_metrics(df):
    """Calcula Possessions, OER, DER i TS%."""
    print("Calculant eficiència avançada (OER/DER)...")
    
    # Possessions: FGA + 0.44*FTA + TOV - ORB
    df['possessions'] = df['fga'] + (0.44 * df['fta']) + df['tov'] - df['orb']
    df['possessions'] = df['possessions'].replace(0, 1)

    # OER (Offensive Efficiency)
    df['oer'] = df['pts'] / df['possessions']
    
    # DER Proxy (Defensive Efficiency)
    df['der_proxy'] = (df['stl'] + df['blk'] + df['drb']) / df['possessions']
    
    # TS% (True Shooting)
    df['ts_pct'] = df['pts'] / (2 * (df['fga'] + 0.44 * df['fta']))
    
    return df

def calc_playstyle_ratios(df):
    """Calcula estil de joc (Ús de tirs i Agressivitat)."""
    print("Calculant perfil de joc (Ràtios)...")
    df['usage_2p'] = df['2pa'] / df['fga'].replace(0, 1)
    df['usage_3p'] = df['3pa'] / df['fga'].replace(0, 1)
    df['ftr'] = df['fta'] / df['fga'].replace(0, 1)
    return df

def calc_spatial_metrics(df):
    """Processa el Shot Chart per calcular volums i eficiències per zona."""
    print("Processant dades espacials (Shot Chart)...")
    
    # Definim Zones
    zones = {
        'paint':   (['rc_pc_a', 'rc_pl_a', 'rc_pr_a'], ['rc_pc_m', 'rc_pl_m', 'rc_pr_m']),
        'mid':     (['rc_mel_a', 'rc_mer_a', 'rc_mbl_a', 'rc_mbr_a'], ['rc_mel_m', 'rc_mer_m', 'rc_mbl_m', 'rc_mbr_m']),
        'corner3': (['rc_c3l_a', 'rc_c3r_a'], ['rc_c3l_m', 'rc_c3r_m']),
        'ab3':     (['rc_ce3l_a', 'rc_ce3r_a', 'rc_e3l_a', 'rc_e3r_a'], ['rc_ce3l_m', 'rc_ce3r_m', 'rc_e3l_m', 'rc_e3r_m'])
    }

    # Calculem Totals (Intents i Encerts) per a cada zona
    for zone_name, (attempts_cols, makes_cols) in zones.items():
        df[f'shots_{zone_name}'] = df[attempts_cols].sum(axis=1)
        df[f'makes_{zone_name}'] = df[makes_cols].sum(axis=1)
        
        # Eficàcia per zona (% Encert)
        df[f'eff_{zone_name}'] = df[f'makes_{zone_name}'] / df[f'shots_{zone_name}'].replace(0, 1)

    # Distribució (% del total de tirs que van a cada zona)
    total_shots = df['shots_paint'] + df['shots_mid'] + df['shots_corner3'] + df['shots_ab3']
    denom = np.where(total_shots > 0, total_shots, df['fga'])

    df['pct_interior_usage'] = df['shots_paint'] / denom
    df['pct_exterior_usage'] = (df['shots_mid'] + df['shots_corner3'] + df['shots_ab3']) / denom
    df['pct_shots_corner3'] = df['shots_corner3'] / denom
    
    return df

# PIPELINE PRINCIPAL
def feature_engineering_pipeline(df):
    """Orquestra totes les transformacions."""
    df = clean_minutes(df)
    df = calc_efficiency_metrics(df)
    df = calc_playstyle_ratios(df)
    df = calc_spatial_metrics(df)
    df = normalize_per_40(df)
    
    # Neteja final de NaNs/Infs
    df = df.replace([np.inf, -np.inf], np.nan).fillna(0)
    return df

def select_final_columns(df):
    """Filtra les columnes finals per al Data Mart."""
    cols_to_keep = [
        # IDs
        'player_feb_id', 'season_id', 'player_name', 'team_name', 'minutes', 'games_played',
        
        # Eficiència
        'oer', 'der_proxy', 'ts_pct',
        
        # Estil
        'usage_2p', 'usage_3p', 'ftr', 
        'pct_interior_usage', 'pct_exterior_usage', 'pct_shots_corner3',
        
        # Eficàcia Zona
        'eff_paint', 'eff_mid', 'eff_corner3', 'eff_ab3',
        
        # Volum P40 (NORMALITZAT)
        'pts_p40', 
        'orb_p40', 'drb_p40', 'trb_p40',
        'ast_p40', 'stl_p40', 'blk_p40', 'tov_p40',
        'pf_p40', 'pfd_p40',
        'fga_p40', '3pa_p40', 'fta_p40'
    ]
    return df[[c for c in cols_to_keep if c in df.columns]]

def main():
    # 1. Load
    df = read_csv_from_azure(INPUT_CONTAINER, INPUT_FILE)
    if df.empty: 
        return

    # 2. Transform
    df_enriched = feature_engineering_pipeline(df)
    
    # 3. Select
    df_gold = select_final_columns(df_enriched)
    
    # 4. Save
    print(f"Dataset Gold generat: {df_gold.shape}")
    upload_csv_to_azure(df_gold, OUTPUT_CONTAINER, OUTPUT_FILE)

if __name__ == "__main__":
    main()
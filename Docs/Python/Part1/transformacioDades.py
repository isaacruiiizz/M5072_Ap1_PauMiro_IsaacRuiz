import pandas as pd
from funcionsAuxiliars import *

# --- CONFIGURACIÓ MESTRA (SCHEMA DEFINITION) ---
STATS_CONFIG = {
    # Identificadors
    'player_name': 'first',
    'team_name': 'first',
    
    # Volum i Joc
    'minutes': 'sum',
    'starter': 'sum',
    'games_played': 'count', 
    
    # Anotació
    'pts': 'sum', 
    'fgm': 'sum', 'fga': 'sum',
    '2pm': 'sum', '2pa': 'sum',
    '3pm': 'sum', '3pa': 'sum',
    'ftm': 'sum', 'fta': 'sum',
    'dunk': 'sum',
    
    # Rebot i Control
    'orb': 'sum', 'drb': 'sum', 'trb': 'sum',
    'ast': 'sum', 'tov': 'sum', 'stl': 'sum',
    'blk': 'sum', 'blka': 'sum',
    'pf': 'sum', 'pfd': 'sum',
    
    # Valoració
    'eff_spanish': 'sum',
    'balance': 'sum',

    # --- ZONES DE TIR (SHOT CHART) ---

    # PINTURA
    'rc_pc_a': 'sum', 'rc_pl_a': 'sum', 'rc_pr_a': 'sum',
    'rc_pc_m': 'sum', 'rc_pl_m': 'sum', 'rc_pr_m': 'sum',
    
    # MITJA DISTÀNCIA
    'rc_mel_a': 'sum', 'rc_mer_a': 'sum', 'rc_mbl_a': 'sum', 'rc_mbr_a': 'sum',
    'rc_mel_m': 'sum', 'rc_mer_m': 'sum', 'rc_mbl_m': 'sum', 'rc_mbr_m': 'sum',
    
    # TRIPLES (Cantonada)
    'rc_c3l_a': 'sum', 'rc_c3r_a': 'sum',
    'rc_c3l_m': 'sum', 'rc_c3r_m': 'sum',
    
    # TRIPLES (Frontal/Altres)
    'rc_ce3l_a': 'sum', 'rc_ce3r_a': 'sum',
    'rc_ce3l_m': 'sum', 'rc_ce3r_m': 'sum',
    'rc_e3l_a': 'sum', 'rc_e3r_a': 'sum',
    'rc_e3l_m': 'sum', 'rc_e3r_m': 'sum'
}

# --- LÒGICA DE NEGOCI ---

def normalize_schema(df, config):
    """Garanteix que totes les columnes del config existeixin."""
    for col in config.keys():
        if col not in df.columns and col != 'games_played':
            if config[col] == 'sum':
                df[col] = 0.0
            else:
                df[col] = "Unknown"
    return df

def clean_data(df, config):
    """Converteix a numèric i omple nuls."""
    cols_to_clean = [k for k, v in config.items() if v == 'sum']
    for col in cols_to_clean:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

def process_stats(df):
    """Processa les estadístiques"""
    print("Processant estadístiques")
    if df.empty: 
        print("No hi ha dades estadístiques a processar")
        return pd.DataFrame()

    # Assegurem que season_id sigui string
    if 'season_id' in df.columns:
        df['season_id'] = df['season_id'].astype(str)

    # 1. Eliminar orfes
    df = df.dropna(subset=['player_feb_id', 'season_id'])
    
    # 2. Schema Evolution
    df = normalize_schema(df, STATS_CONFIG)
    
    # 3. Conversió a numèric
    df = clean_data(df, STATS_CONFIG)
    
    # 4. Agrupació
    agg_rules = {k:v for k,v in STATS_CONFIG.items() if k != 'games_played'}
    
    df_grouped = df.groupby(['player_feb_id', 'season_id']).agg(agg_rules).reset_index()
    
    # 5. Comptar partits reals
    df_counts = df.groupby(['player_feb_id', 'season_id']).size().reset_index(name='games_played')
    df_grouped = pd.merge(df_grouped, df_counts, on=['player_feb_id', 'season_id'])
    
    # 6. Filtre de qualitat (>50 minuts)
    original_count = len(df_grouped)
    df_clean = df_grouped[df_grouped['minutes'] > 50].copy()
    print(f"   - Jugadors filtrats: {original_count} -> {len(df_clean)} (Minuts > 50)")
    
    return df_clean

def process_shots(df):
    """Processa les cartes de tirs"""
    print("Processant carta de tirs")
    if df.empty: 
        print("No hi ha dades de tirs a processar")
        return pd.DataFrame()
    
    if 'season_id' in df.columns:
        df['season_id'] = df['season_id'].astype(str)
        
    df = df.dropna(subset=['player_feb_id', 'season_id'])
    
    # Agrupem per season_id
    shots_agg = df.groupby(['player_feb_id', 'season_id']).size().reset_index(name='total_shots_recorded')
    return shots_agg

def main():
    # 1. Llegir Bronze
    df_stats = read_csv_from_azure("01-bronze", "feb_raw_statistics.csv")
    df_shots = read_csv_from_azure("01-bronze", "feb_raw_shots.csv")

    # 2. Transformar
    df_stats_clean = process_stats(df_stats)
    df_shots_agg = process_shots(df_shots)

    if df_stats_clean.empty:
        print("Error: Dataset d'estadístiques buit.")
        return

    # 3. Fusionar (Join)
    print("Fusionant dades")
    df_silver = pd.merge(
        df_stats_clean,
        df_shots_agg,
        on=['player_feb_id', 'season_id'],
        how='left'
    )
    df_silver['total_shots_recorded'] = df_silver['total_shots_recorded'].fillna(0)

    # 4. Guardar a Silver
    upload_csv_to_azure(df_silver, "02-silver", "feb_silver_dataset.csv")

if __name__ == "__main__":
    main()
# Importem les llibreries necessàries
import os
import pandas as pd
from io import StringIO
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Importem la nostra funció de connexió personalitzada
from connMongo import get_db_connection

# Carreguem les variables d'entorn
load_dotenv()

def upload_to_azure_bronze(df, filename):
    """
    Puja un DataFrame a la capa BRONZE d'Azure utilitzant un buffer en memòria.
    No es crea cap fitxer local temporal.
    """
    try:
        # 1. Recuperar la cadena de connexió
        connect_str = os.getenv('AZURE_CONNECTION_STRING')
        if not connect_str:
            raise ValueError("Error: No s'ha trobat AZURE_CONNECTION_STRING al fitxer .env")

        # 2. Connectar al client de Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_name = "01-bronze"
        
        # 3. Convertir DataFrame a CSV en memòria (Buffer)
        output = StringIO()
        df.to_csv(output, index=False)
        csv_data = output.getvalue()

        # 4. Pujar al contenidor
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
        print(f"Pujant '{filename}' a Azure Bronze ({len(csv_data)/1024:.2f} KB)...")
        
        blob_client.upload_blob(csv_data, overwrite=True)
        print("Pujada completada amb èxit!")
        
    except Exception as e:
        print(f"Error crític pujant a Azure: {e}")

def main():
    db = get_db_connection()
    
    # LLISTA DE COL·LECCIONS A BAIXAR
    collections_to_extract = [
        "FEB3_players_statistics",
        "FEB3_players_shots" 
    ]
    
    # Filtre per temporada i competició
    query = {"competition_name": {"$regex": "FEB3|EBA", "$options": "i"}}
    projection = {"_id": 0}

    # Bucle per baixar les col·leccions
    for col_name in collections_to_extract:
        print(f"Processant col·lecció: {col_name}...")
        
        collection = db[col_name]
        cursor = collection.find(query, projection)
        df = pd.DataFrame(list(cursor))

        # Validem si la col·lecció està buida
        if df.empty:
            print(f"La col·lecció {col_name} no té dades per aquest filtre o està buida.")
            continue

        print(f"{len(df)} registres baixats.")
        
        # Generem un nom de fitxer dinàmic: 'feb_raw_statistics.csv', 'feb_raw_shots.csv'
        # Split per agafar l'última part del nom (statistics o shots)
        suffix = col_name.split('_')[-1] 
        file_name = f"feb_raw_{suffix}.csv"
        
        # Pujem al Azure
        upload_to_azure_bronze(df, file_name)

    print("Procés finalitzat per a totes les col·leccions.")

if __name__ == "__main__":
    main()
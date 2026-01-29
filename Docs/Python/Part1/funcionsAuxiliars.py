import tempfile
import os
import pandas as pd
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from io import StringIO

load_dotenv()

def get_blob_client(container, filename):
    connect_str = os.getenv('AZURE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    return blob_service_client.get_blob_client(container=container, blob=filename)

def read_csv_from_azure(container, filename):
    print(f"Descarregant '{filename}' de {container}...")
    blob_client = get_blob_client(container, filename)

    # 1. Creem un fitxer temporal al disc dur
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        print(f"Guardant temporalment a disc...")
        
        try:
            # 2. Descarreguem directament al fitxer
            with open(tmp_file.name, "wb") as file_handle:
                download_stream = blob_client.download_blob()
                download_stream.readinto(file_handle)
            
            print("Descàrrega finalitzada. Llegint CSV...")
            
            # 3. Llegim amb Pandas des del disc
            df = pd.read_csv(tmp_file.name, low_memory=False)
            
        except Exception as e:
            print(f"Error durant la descàrrega/lectura: {e}")
            return pd.DataFrame()
            
        finally:
            # Tanquem el fitxer
            try: tmp_file.close()
            except: pass

    # 4. Esborrem el fitxer temporal
    try: os.remove(tmp_file.name)
    except: pass
        
    return df

def upload_csv_to_azure(df, container, filename):
    output = StringIO()
    df.to_csv(output, index=False)
    print(f"Pujant '{filename}' a {container} ({len(df)} files)...")
    
    blob_client = get_blob_client(container, filename)
    blob_client.upload_blob(output.getvalue(), overwrite=True)
    print("Càrrega completada")
import pymongo
import sys
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
    DB_NAME = "feb_db"

    try:
        print(f"🔌 Connectant a {MONGO_HOST}:{MONGO_PORT}...")
        client = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT, serverSelectionTimeoutMS=5000)
        client.server_info()
        db = client[DB_NAME]
        print(f"✅ Connectat a '{DB_NAME}'")
        return db
    except Exception as e:
        print(f"❌ Error de connexió: {e}")
        sys.exit(1)

get_db_connection()
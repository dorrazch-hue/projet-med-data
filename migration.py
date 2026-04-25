import pandas as pd
import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def migrate_data():
    print("--- 🚀 MIGRATION OPTIMISÉE PAR BATCHS (CHUNKS) ---")
    
    uri = os.getenv("MONGODB_URI")
    if not uri:
        print("❌ ERREUR : MONGODB_URI manquante.")
        sys.exit(1)

    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        db = client.get_database()
        collection = db['patients']
        collection.delete_many({}) # Nettoyage initial

        cols = ['Name', 'Age', 'Gender', 'Blood Type', 'Medical Condition']
        
        # Utilisation de chunksize pour la performance mémoire (Étape 6)
        chunk_size = 5000
        reader = pd.read_csv('healthcare_dataset.csv', usecols=cols, chunksize=chunk_size)

        total_inserted = 0
        for i, chunk in enumerate(reader):
            # Nettoyage par chunk
            chunk['Name'] = chunk['Name'].astype(str).str.strip()
            chunk['Age'] = pd.to_numeric(chunk['Age'], errors='coerce').fillna(0).astype(int)
            chunk = chunk.fillna("Unknown")
            chunk = chunk.drop_duplicates(subset=['Name', 'Age'])

            # Insertion
            if not chunk.empty:
                payload = chunk.to_dict('records')
                collection.insert_many(payload)
                total_inserted += len(chunk)
                print(f"📦 Chunk {i+1} traité : {len(chunk)} documents insérés.")

        print(f"✅ Migration terminée ! Total : {total_inserted} documents en base.")

    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    migrate_data()

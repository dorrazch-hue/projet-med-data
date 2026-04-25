import pandas as pd
import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def migrate_data():
    uri = os.getenv("MONGODB_URI")
    if not uri:
        print("❌ ERREUR : MONGODB_URI manquante.")
        sys.exit(1)

    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        db = client.get_database()
        collection = db['patients']

        # CONTRÔLE ÉTAPE 5
        cols = ['Name', 'Age', 'Gender', 'Blood Type', 'Medical Condition']
        df = pd.read_csv('healthcare_dataset.csv', usecols=cols)
        
        df['Name'] = df['Name'].astype(str).str.strip()
        df['Age'] = pd.to_numeric(df['Age'], errors='coerce').fillna(0).astype(int)
        df = df.fillna("Unknown")

        initial_count = len(df)
        df = df.drop_duplicates(subset=['Name', 'Age'])
        
        print(f"✅ Nettoyage : {initial_count - len(df)} doublons supprimés.")

        payload = df.to_dict('records')
        collection.delete_many({}) 
        collection.insert_many(payload)
        print(f"🚀 Migration réussie : {len(df)} documents insérés.")

    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    migrate_data()

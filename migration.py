import pandas as pd
import os
import sys
from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv

load_dotenv()

def migrate_data():
    print("--- 🚀 MIGRATION AVEC VÉRIFICATION DES INDEX ---")
    
    uri = os.getenv("MONGODB_URI")
    if not uri:
        print("❌ ERREUR : MONGODB_URI manquante.")
        sys.exit(1)

    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        db = client.get_database()
        collection = db['patients']

        # 1. PRÉPARATION & NETTOYAGE
        cols = ['Name', 'Age', 'Gender', 'Blood Type', 'Medical Condition']
        df = pd.read_csv('healthcare_dataset.csv', usecols=cols)
        df['Name'] = df['Name'].astype(str).str.strip()
        df = df.drop_duplicates(subset=['Name', 'Age'])

        # 2. INSERTION
        payload = df.to_dict('records')
        collection.delete_many({}) 
        collection.insert_many(payload)
        print(f"🚀 {len(df)} documents insérés.")

        # 3. GESTION DES INDEX (Étape 8)
        print("🔍 Vérification des index...")
        # Création d'un index ascendant sur le champ 'Name'
        collection.create_index([("Name", ASCENDING)])
        
        # Affichage des index pour preuve
        indexes = collection.list_indexes()
        print("✅ Index actifs sur la collection :")
        for idx in indexes:
            print(f" - {idx['name']}")

    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    migrate_data()

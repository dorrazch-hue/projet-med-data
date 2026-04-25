import pandas as pd
import os
import time
import sys
from pymongo import MongoClient

try:
    print("--- Début de la migration sécurisée ---")
    
    # SÉCURITÉ : Pas de fallback admin:admin
    uri = os.getenv("MONGODB_URI")
    
    if not uri:
        print("❌ ERREUR CRITIQUE : La variable d'environnement MONGODB_URI est manquante.")
        sys.exit(1)

    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    
    # Attente de disponibilité
    for i in range(5):
        try:
            client.admin.command('ping')
            print("✅ MongoDB est prêt !")
            break
        except:
            print(f"⏳ Attente MongoDB ({i+1}/5)...")
            time.sleep(3)

    db = client.get_database()
    collection = db['patients']
    
    # Nettoyage pour éviter les doublons
    collection.delete_many({}) 

    # Migration
    df = pd.read_csv('healthcare_dataset.csv')
    print(f"Insertion de {len(df)} lignes...")
    collection.insert_many(df.to_dict(orient='records'))
    
    print("--- MIGRATION RÉUSSIE ---")
    
except Exception as e:
    print(f"❌ ERREUR : {e}")
    sys.exit(1)

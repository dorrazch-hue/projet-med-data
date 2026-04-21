import pandas as pd
import os
import time
from pymongo import MongoClient

try:
    print("--- Début de la migration robuste et performante ---")
    
    # 1. Connexion sécurisée
    uri = os.getenv("MONGODB_URI", "mongodb://admin:admin@mongodb:27017/")
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    
    # --- ROBUSTESSE : Attente de disponibilité de la base ---
    print("Vérification de la disponibilité de MongoDB...")
    for i in range(10):
        try:
            client.admin.command('ping')
            print("✅ MongoDB est prêt !")
            break
        except Exception:
            print(f"⏳ MongoDB n'est pas encore prêt ({i+1}/10)... attente de 3s")
            time.sleep(3)
    else:
        raise Exception("Impossible de se connecter à MongoDB après 30 secondes.")

    db = client.get_database()
    collection = db['patients']
    
    # 2. FIABILISATION : Idempotence (on évite les doublons)
    print("Nettoyage des anciennes données...")
    collection.delete_many({}) 

    # --- PERFORMANCE : Création des Index ---
    print("Optimisation des performances (création des index)...")
    collection.create_index([("Name", 1)])              # Recherche par nom
    collection.create_index([("Medical Condition", 1)]) # Statistiques par maladie
    collection.create_index([("Hospital", 1)])          # Filtres par hôpital
    print("✅ Index créés avec succès.")

    # 3. Migration des données
    print("Lecture du fichier CSV...")
    df = pd.read_csv('healthcare_dataset.csv')
    
    print(f"Insertion de {len(df)} lignes en cours...")
    collection.insert_many(df.to_dict(orient='records'))
    
    print("--- MIGRATION RÉUSSIE, SÉCURISÉE ET OPTIMISÉE ! ---")
    
except Exception as e:
    print(f"❌ ERREUR CRITIQUE : {e}")
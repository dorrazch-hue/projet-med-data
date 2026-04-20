import pandas as pd
import os
from pymongo import MongoClient

try:
    print("--- Tentative de connexion sécurisée ---")
    
    # Récupération de l'URI depuis les variables d'environnement (configurées dans docker-compose)
    uri = os.getenv("MONGODB_URI", "mongodb://admin:admin@mongodb:27017/")
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    
    # Connexion à la base de données
    db = client.get_database()
    collection = db['patients']
    
    print("Lecture du fichier CSV...")
    df = pd.read_csv('healthcare_dataset.csv')
    
    print(f"Début de la migration de {len(df)} lignes...")
    # Insertion par lots pour la performance
    collection.insert_many(df.to_dict(orient='records'))
    
    print("--- MIGRATION RÉUSSIE AVEC SUCCÈS ! ---")
    
except Exception as e:
    print(f"ERREUR : {e}")
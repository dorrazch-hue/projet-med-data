import pandas as pd
from pymongo import MongoClient

try:
    print("--- Tentative de connexion (Reset) ---")
    # On utilise 'mongodb' qui est le nom du service dans ton YAML
    client = MongoClient('mongodb://admin:admin@mongodb:27017/', serverSelectionTimeoutMS=5000)
    
    db = client['healthcare']
    collection = db['patients']
    
    print("Lecture du fichier CSV...")
    df = pd.read_csv('healthcare_dataset.csv')
    
    print(f"Envoi de {len(df)} lignes...")
    collection.insert_many(df.to_dict(orient='records'))
    
    print("--- MIGRATION RÉUSSIE AVEC SUCCÈS ! ---")
    
except Exception as e:
    print(f"ERREUR : {e}")

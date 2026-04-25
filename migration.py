import pandas as pd
import os
import time
import sys
from pymongo import MongoClient

try:
    print("--- 🧹 DÉBUT DE LA MIGRATION AVEC NETTOYAGE DES DONNÉES ---")
    
    # SÉCURITÉ
    uri = os.getenv("MONGODB_URI")
    if not uri:
        print("❌ ERREUR : MONGODB_URI manquante.")
        sys.exit(1)

    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    db = client.get_database()
    collection = db['patients']

    # 1. CHARGEMENT
    print("Chargement du fichier CSV...")
    df = pd.read_csv('healthcare_dataset.csv')
    initial_count = len(df)

    # 2. NETTOYAGE (Priorité 5)
    print("Nettoyage en cours...")
    
    # Suppression des doublons basés sur le nom et l'âge
    df = df.drop_duplicates(subset=['Name', 'Age'])
    
    # Sélection des colonnes pertinentes
    colonnes_utiles = ['Name', 'Age', 'Gender', 'Blood Type', 'Medical Condition']
    df = df[colonnes_utiles]
    
    # Nettoyage des chaînes de caractères (espaces en trop)
    df['Name'] = df['Name'].str.strip()
    
    final_count = len(df)
    print(f"✅ {initial_count - final_count} doublons supprimés.")
    print(f"✅ Colonnes conservées : {colonnes_utiles}")

    # 3. MIGRATION
    print("Nettoyage de la base de données...")
    collection.delete_many({}) 

    print(f"Insertion de {final_count} documents nettoyés...")
    collection.insert_many(df.to_dict(orient='records'))
    
    print("--- 🏆 MIGRATION RÉUSSIE ET DONNÉES PROPRES ---")
    
except Exception as e:
    print(f"❌ ERREUR : {e}")
    sys.exit(1)

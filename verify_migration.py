import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def verify():
    # Vérification de l'URI pour éviter le fallback admin:admin
    uri = os.getenv("MONGODB_URI")
    if not uri:
        print("❌ ERREUR : MONGODB_URI manquante dans le .env")
        return

    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=2000)
        db = client.get_database()
        col = db['patients']
        
        print("--- 🔍 RAPPORT D'INTÉGRITÉ POST-MIGRATION ---")
        
        # 1. Comptage (Point 3)
        count = col.count_documents({})
        print(f"✅ Documents en base : {count}")
        
        # 2. Vérification des Index (Point 10)
        print("\n✅ Index détectés :")
        for name, info in col.index_information().items():
            print(f" - {name}")

        # 3. Échantillon de typage (Point 2 & 3)
        sample = col.find_one()
        if sample:
            print("\n✅ Analyse d'un document type (Validation des types) :")
            for key, value in sample.items():
                # On affiche le type Python pour prouver le cast (int, str, etc.)
                print(f" - {key}: {type(value).__name__} (Valeur: {value})")
                
    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")

if __name__ == "__main__":
    verify()

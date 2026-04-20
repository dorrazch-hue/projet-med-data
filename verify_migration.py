import os
import pandas as pd
from pymongo import MongoClient

try:
    # 1. Utilisation de l'URI sécurisée (Variable d'environnement)
    uri = os.getenv("MONGODB_URI", "mongodb://admin:admin@mongodb:27017/")
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    
    db = client.get_database()
    collection = db['patients']

    print("--- 🔍 VÉRIFICATION DES DONNÉES ---")

    # 2. On compte les entrées dans MongoDB
    total_mongo = collection.count_documents({})
    
    # 3. On compte les lignes du fichier CSV pour comparer dynamiquement
    df = pd.read_csv('healthcare_dataset.csv')
    total_csv = len(df)

    print(f"Nombre d'entrées dans MongoDB : {total_mongo}")
    print(f"Nombre de lignes dans le CSV  : {total_csv}")

    # 4. Comparaison intelligente
    if total_mongo == total_csv:
        print("✅ SUCCÈS : La migration est intègre (MongoDB == CSV) !")
    else:
        print(f"⚠️ ATTENTION : Différence détectée ! ({total_mongo} en base vs {total_csv} dans le fichier)")

    # 5. Test de lecture
    exemple = collection.find_one()
    if exemple:
        print(f"✅ TEST LECTURE : Patient trouvé -> {exemple.get('Name')}")

except Exception as e:
    print(f"❌ ERREUR LORS DU TEST : {e}")
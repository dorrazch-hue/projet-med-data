import pandas as pd
from pymongo import MongoClient

try:
    # Connexion à la base
    client = MongoClient('mongodb://admin:admin@mongodb_container:27017/')
    db = client['healthcare']
    collection = db['patients']

    print("--- 🔍 VÉRIFICATION DES DONNÉES ---")

    # 1. On compte les documents
    total_mongo = collection.count_documents({})
    print(f"Nombre d'entrées dans MongoDB : {total_mongo}")

    # 2. On compare avec le chiffre attendu
    if total_mongo == 55500:
        print("✅ SUCCÈS : Toutes les données sont présentes !")
    else:
        print(f"⚠️ ATTENTION : Il y a {total_mongo} entrées au lieu de 55500.")

    # 3. On affiche un exemple pour vérifier le contenu
    exemple = collection.find_one()
    if exemple:
        print(f"✅ TEST LECTURE : Patient trouvé -> {exemple.get('Name')} (Diagnostic: {exemple.get('Medical Condition')})")

except Exception as e:
    print(f"❌ ERREUR LORS DU TEST : {e}")

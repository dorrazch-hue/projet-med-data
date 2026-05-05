import os
import sys
from pymongo import MongoClient
from pymongo.errors import OperationFailure
from dotenv import load_dotenv

load_dotenv()


def check_users():
    print("\n── 1. Liste des utilisateurs MongoDB (db.getUsers()) ──")
    uri = f"mongodb://{os.getenv('MONGO_ROOT_USER')}:{os.getenv('MONGO_ROOT_PASSWORD')}@mongodb:27017/admin"
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    db = client[os.getenv("DATABASE_NAME")]
    users = db.command("usersInfo")
    for u in users.get("users", []):
        roles = [r["role"] for r in u.get("roles", [])]
        print(f"  👤 {u['user']} → rôles : {roles}")
    client.close()


def check_auditor_cannot_write():
    print("\n── 2. Tentative d'écriture avec le compte auditor ──")
    db_name = os.getenv("DATABASE_NAME")
    uri = f"mongodb://{os.getenv('MONGO_AUDIT_USER')}:{os.getenv('MONGO_AUDIT_PASSWORD')}@mongodb:27017/{db_name}"
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    col = client[db_name]["patients"]

    count = col.count_documents({})
    print(f"  ✅ Lecture autorisée — {count} documents visibles")

    try:
        col.insert_one({"test": "should_fail"})
        print("  ❌ ERREUR : l'écriture a réussi — vérifier le rôle !")
    except OperationFailure as e:
        print(f"  ✅ Écriture refusée comme attendu : {e.details.get('codeName', e)}")
    client.close()


def check_unauthenticated_access():
    print("\n── 3. Tentative d'accès sans authentification ──")
    db_name = os.getenv("DATABASE_NAME")
    uri = f"mongodb://mongodb:27017/{db_name}"
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    try:
        count = client[db_name]["patients"].count_documents({})
        print(f"  ❌ ERREUR : accès non authentifié autorisé ({count} docs) !")
    except Exception as e:
        print(f"  ✅ Accès refusé comme attendu : {type(e).__name__}")
    client.close()


if __name__ == "__main__":
    print("=" * 55)
    print("   PREUVES DE SÉCURITÉ RBAC")
    print("=" * 55)
    check_users()
    check_auditor_cannot_write()
    check_unauthenticated_access()
    print("\n✅ Audit de sécurité terminé.")
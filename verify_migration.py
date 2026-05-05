import os
import sys
import logging
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs_verification.txt", mode="w", encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)

EXPECTED_BLOCKS = [
    "personal_info", "medical_info", "admission_info",
    "administrative_info", "metadata",
]

EXPECTED_INDEXES = {
    "_id_", "idx_name", "idx_condition", "idx_hospital",
    "idx_doctor", "idx_admission_date", "idx_hospital_date",
}

DEDUP_PIPELINE = [
    {
        "$group": {
            "_id": {
                "name":           "$personal_info.name",
                "age":            "$personal_info.age",
                "doctor":         "$admission_info.doctor",
                "hospital":       "$admission_info.hospital",
                "admission_date": "$admission_info.admission_date",
            },
            "count": {"$sum": 1},
        }
    },
    {"$match": {"count": {"$gt": 1}}},
]


def verify():
    log.info("=" * 55)
    log.info("   RAPPORT D'INTÉGRITÉ POST-MIGRATION")
    log.info("=" * 55)

    uri = os.getenv("MONGODB_URI")
    if not uri:
        log.error("MONGODB_URI manquante dans .env — arrêt.")
        sys.exit(1)

    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    db = client.get_database()
    col = db["patients"]

    # 1. Nombre de documents
    total = col.count_documents({})
    log.info(f"Documents en base                   : {total}")

    # 2. Doublons résiduels
    duplicates = list(col.aggregate(DEDUP_PIPELINE))
    if duplicates:
        log.warning(f"Doublons résiduels détectés         : {len(duplicates)}")
    else:
        log.info("Doublons résiduels                  : 0 ✅")

    # 3. Blocs imbriqués manquants
    missing_blocks = 0
    for block in EXPECTED_BLOCKS:
        count_missing = col.count_documents({block: {"$exists": False}})
        if count_missing > 0:
            log.warning(f"Bloc '{block}' absent dans {count_missing} document(s)")
            missing_blocks += count_missing
    if missing_blocks == 0:
        log.info("Blocs imbriqués                     : tous présents ✅")

    # 4. Types attendus (500 docs)
    type_errors = 0
    sample = list(col.find({}, {"personal_info": 1, "admission_info": 1}).limit(500))
    for doc in sample:
        pi = doc.get("personal_info", {})
        ai = doc.get("admission_info", {})
        if not isinstance(pi.get("age"), int):
            type_errors += 1
        if not isinstance(ai.get("room_number"), int):
            type_errors += 1
        if not isinstance(ai.get("admission_date"), datetime):
            type_errors += 1
        if not isinstance(ai.get("discharge_date"), datetime):
            type_errors += 1

    if type_errors == 0:
        log.info("Validation des types (500 docs)     : OK ✅")
    else:
        log.warning(f"Erreurs de type détectées           : {type_errors}")

    # 5. Index attendus
    existing_indexes = set(col.index_information().keys())
    missing_indexes = EXPECTED_INDEXES - existing_indexes
    if missing_indexes:
        log.warning(f"Index manquants                     : {missing_indexes}")
    else:
        log.info("Index                               : tous présents ✅")
    log.info(f"Index actifs : {sorted(existing_indexes)}")

    # 6. Statistiques valeurs invalides
    null_names   = col.count_documents({"personal_info.name":                {"$in": [None, "Unknown", ""]}})
    null_cond    = col.count_documents({"medical_info.condition":            {"$in": [None, "Unknown", ""]}})
    zero_billing = col.count_documents({"administrative_info.billing_amount": 0})
    log.info(f"Noms inconnus / vides               : {null_names}")
    log.info(f"Conditions médicales inconnues      : {null_cond}")
    log.info(f"Montants de facturation à 0         : {zero_billing}")

    log.info("=" * 55)
    log.info("Vérification terminée. Rapport dans logs_verification.txt")


if __name__ == "__main__":
    verify()
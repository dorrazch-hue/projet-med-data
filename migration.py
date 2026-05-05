import pandas as pd
import os
import sys
import logging
from datetime import datetime, timezone
from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs_migration.txt", mode="w", encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)

CSV_FILE = "healthcare_dataset.csv"
CHUNK_SIZE = 5000

CSV_COLS = [
    "Name", "Age", "Gender", "Blood Type", "Medical Condition",
    "Date of Admission", "Discharge Date", "Doctor", "Hospital",
    "Insurance Provider", "Billing Amount", "Room Number",
    "Admission Type", "Medication", "Test Results",
]


def build_document(row: dict):
    try:
        age = int(pd.to_numeric(row.get("Age"), errors="coerce") or 0)
        room_number = int(pd.to_numeric(row.get("Room Number"), errors="coerce") or 0)

        billing_raw = pd.to_numeric(row.get("Billing Amount"), errors="coerce")
        billing = float(billing_raw) if pd.notna(billing_raw) and billing_raw >= 0 else 0.0

        admission_date = pd.to_datetime(row.get("Date of Admission"), errors="coerce")
        discharge_date = pd.to_datetime(row.get("Discharge Date"), errors="coerce")

        if pd.isna(admission_date) or pd.isna(discharge_date):
            return None

        admission_dt = admission_date.to_pydatetime()
        discharge_dt = discharge_date.to_pydatetime()
        duration_days = (discharge_dt - admission_dt).days

        return {
            "personal_info": {
                "name":       str(row.get("Name") or "Unknown").strip(),
                "age":        age,
                "gender":     str(row.get("Gender") or "Unknown").strip(),
                "blood_type": str(row.get("Blood Type") or "Unknown").strip(),
            },
            "medical_info": {
                "condition":    str(row.get("Medical Condition") or "Unknown").strip(),
                "medication":   str(row.get("Medication") or "Unknown").strip(),
                "test_results": str(row.get("Test Results") or "Unknown").strip(),
            },
            "admission_info": {
                "admission_date": admission_dt,
                "discharge_date": discharge_dt,
                "admission_type": str(row.get("Admission Type") or "Unknown").strip(),
                "room_number":    room_number,
                "doctor":         str(row.get("Doctor") or "Unknown").strip(),
                "hospital":       str(row.get("Hospital") or "Unknown").strip(),
                "duration_days":  duration_days,
            },
            "administrative_info": {
                "insurance_provider": str(row.get("Insurance Provider") or "Unknown").strip(),
                "billing_amount":     billing,
            },
            "metadata": {
                "source_file":          CSV_FILE,
                "migrated_at":          datetime.now(timezone.utc),
                "is_duplicate_removed": False,
            },
        }
    except Exception as exc:
        log.warning(f"Ligne rejetée : {exc}")
        return None


def migrate_data():
    log.info("=" * 55)
    log.info("   DÉMARRAGE DU PIPELINE DE MIGRATION MONGODB")
    log.info("=" * 55)

    uri = os.getenv("MONGODB_URI")
    if not uri:
        log.error("MONGODB_URI manquante dans le fichier .env — arrêt.")
        sys.exit(1)

    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    db = client.get_database()
    collection = db["patients"]

    if not os.path.exists(CSV_FILE):
        log.error(f"Fichier introuvable : {CSV_FILE}")
        sys.exit(1)

    df_full = pd.read_csv(CSV_FILE, usecols=CSV_COLS)
    total_source = len(df_full)
    log.info(f"Lignes lues depuis le CSV : {total_source}")

    dedup_key = ["Name", "Age", "Doctor", "Hospital", "Date of Admission"]
    df_deduped = df_full.drop_duplicates(subset=dedup_key)
    duplicates_removed = total_source - len(df_deduped)
    log.info(f"Doublons détectés et supprimés : {duplicates_removed}")

    collection.delete_many({})
    total_inserted = 0
    total_rejected = 0

    for chunk_start in range(0, len(df_deduped), CHUNK_SIZE):
        chunk = df_deduped.iloc[chunk_start: chunk_start + CHUNK_SIZE]
        documents = []

        for row in chunk.to_dict("records"):
            doc = build_document(row)
            if doc is None:
                total_rejected += 1
            else:
                documents.append(doc)

        if documents:
            collection.insert_many(documents)
            total_inserted += len(documents)
            log.info(f"Chunk inséré : {len(documents)} documents (total : {total_inserted})")

    log.info("Création des index...")
    collection.create_index([("personal_info.name", ASCENDING)], name="idx_name")
    collection.create_index([("medical_info.condition", ASCENDING)], name="idx_condition")
    collection.create_index([("admission_info.hospital", ASCENDING)], name="idx_hospital")
    collection.create_index([("admission_info.doctor", ASCENDING)], name="idx_doctor")
    collection.create_index([("admission_info.admission_date", ASCENDING)], name="idx_admission_date")
    collection.create_index(
        [("admission_info.hospital", ASCENDING), ("admission_info.admission_date", ASCENDING)],
        name="idx_hospital_date"
    )
    log.info("Index créés avec succès.")

    log.info("=" * 55)
    log.info("   RAPPORT FINAL DE MIGRATION")
    log.info("=" * 55)
    log.info(f"Lignes source (CSV) : {total_source}")
    log.info(f"Doublons détectés : {duplicates_removed}")
    log.info(f"Lignes invalides rejetées : {total_rejected}")
    log.info(f"Documents migrés en base : {total_inserted}")
    log.info("=" * 55)


if __name__ == "__main__":
    migrate_data()
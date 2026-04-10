import pandas as pd
from pymongo import MongoClient

# ===== CONFIG =====
CSV_FILE = "healthcare_dataset.csv"
MONGO_URI = "mongodb://127.0.0.1:27017/"
DB_NAME = "healthcare"
COLLECTION_NAME = "patients"

# ===== CONNEXION MONGODB =====
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# ===== LECTURE CSV =====
df = pd.read_csv(CSV_FILE)

# ===== NETTOYAGE / CONVERSIONS =====
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
df["Billing Amount"] = pd.to_numeric(df["Billing Amount"], errors="coerce")
df["Room Number"] = pd.to_numeric(df["Room Number"], errors="coerce")

df["Date of Admission"] = pd.to_datetime(df["Date of Admission"], errors="coerce")
df["Discharge Date"] = pd.to_datetime(df["Discharge Date"], errors="coerce")

df = df.dropna()

# ===== INSERTION =====
records = df.to_dict(orient="records")
result = collection.insert_many(records)

print(f"✅ Migration terminée : {len(result.inserted_ids)} documents insérés")

import os
import pytest
import pandas as pd
from datetime import datetime
from migration import build_document


def make_row(**kwargs):
    base = {
        "Name": "Alice Martin",
        "Age": "30",
        "Gender": "F",
        "Blood Type": "A+",
        "Medical Condition": "Diabetes",
        "Date of Admission": "2023-01-15",
        "Discharge Date": "2023-01-22",
        "Doctor": "Dr. Smith",
        "Hospital": "City Hospital",
        "Insurance Provider": "Aetna",
        "Billing Amount": "12500.50",
        "Room Number": "101",
        "Admission Type": "Elective",
        "Medication": "Insulin",
        "Test Results": "Normal",
    }
    base.update(kwargs)
    return base


class TestBuildDocument:

    def test_structure_blocs(self):
        doc = build_document(make_row())
        assert doc is not None
        for bloc in ["personal_info", "medical_info", "admission_info",
                     "administrative_info", "metadata"]:
            assert bloc in doc

    def test_types_numeriques(self):
        doc = build_document(make_row(Age="42", **{"Room Number": "205"}))
        assert isinstance(doc["personal_info"]["age"], int)
        assert isinstance(doc["admission_info"]["room_number"], int)

    def test_types_dates(self):
        doc = build_document(make_row())
        assert isinstance(doc["admission_info"]["admission_date"], datetime)
        assert isinstance(doc["admission_info"]["discharge_date"], datetime)

    def test_duration_days(self):
        doc = build_document(make_row(
            **{"Date of Admission": "2023-01-15", "Discharge Date": "2023-01-22"}
        ))
        assert doc["admission_info"]["duration_days"] == 7

    def test_billing_negatif_remis_a_zero(self):
        doc = build_document(make_row(**{"Billing Amount": "-500"}))
        assert doc["administrative_info"]["billing_amount"] == 0.0

    def test_billing_valide(self):
        doc = build_document(make_row(**{"Billing Amount": "12500.50"}))
        assert isinstance(doc["administrative_info"]["billing_amount"], float)
        assert doc["administrative_info"]["billing_amount"] == 12500.50

    def test_nom_strippé(self):
        doc = build_document(make_row(Name="  Bob Dupont  "))
        assert doc["personal_info"]["name"] == "Bob Dupont"

    def test_date_invalide_retourne_none(self):
        doc = build_document(make_row(**{"Date of Admission": "not-a-date"}))
        assert doc is None

    def test_metadata_source_file(self):
        doc = build_document(make_row())
        assert doc["metadata"]["source_file"] == "healthcare_dataset.csv"

    def test_condition_inconnue_par_defaut(self):
        doc = build_document(make_row(**{"Medical Condition": None}))
        assert doc["medical_info"]["condition"] == "Unknown"


@pytest.mark.integration
class TestIntegration:

    def get_collection(self):
        from pymongo import MongoClient
        from dotenv import load_dotenv
        load_dotenv()
        uri = os.getenv("MONGODB_URI")
        if not uri:
            pytest.skip("MONGODB_URI non définie.")
        client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        db = client.get_database()
        return db["patients"]

    def test_collection_non_vide(self):
        col = self.get_collection()
        assert col.count_documents({}) > 0

    def test_structure_document(self):
        col = self

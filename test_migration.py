import pandas as pd
import pytest

def clean_data_logic(df):
    """Logique de nettoyage extraite pour le test"""
    df['Name'] = df['Name'].astype(str).str.strip()
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce').fillna(0).astype(int)
    df = df.fillna("Unknown")
    df = df.drop_duplicates(subset=['Name', 'Age'])
    return df

def test_cleaning_logic():
    data = {
        'Name': [' Alice ', 'Alice', 'Bob'],
        'Age': [25, 25, 'invalid'],
        'Gender': ['F', 'F', 'M'],
        'Blood Type': ['A+', 'A+', None],
        'Medical Condition': ['Cold', 'Cold', 'Flu']
    }
    df = pd.DataFrame(data)
    df_cleaned = clean_data_logic(df)
    
    assert len(df_cleaned) == 2
    assert df_cleaned.iloc[0]['Name'] == "Alice"
    assert df_cleaned.iloc[1]['Age'] == 0
    assert df_cleaned.iloc[1]['Blood Type'] == "Unknown"

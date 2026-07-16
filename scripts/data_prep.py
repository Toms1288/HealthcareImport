import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime as dt

# Fonction pour nettoyer les données
def clean_data(file_path):
    data = pd.read_csv(file_path)

    # Supprimer les doublons
    print(f"Nombre de lignes en doublon supprimées : {data.duplicated().sum()}")
    data = data.drop_duplicates()
    # Ajout d'un index unique pour chaque patient
    data['patient_id'] = data.index
    # Renommer les colonnes pour plus de clarté
    data = data.rename(columns={"patient_id":"patient_id","Name":"name","Age":"age","Gender":"gender","Blood Type":"blood_type",
            "Medical Condition":"medical_condition","Date of Admission":"date_of_admission","Doctor":"doctor","Hospital":"hospital","Insurance Provider":"insurance_provider",
            "Billing Amount":"billing_amount","Room Number":"room_number","Admission Type":"admission_type","Discharge Date":"discharge_date","Medication":"medication","Test Results":"test_results"})
     # Normaliser les noms, suppression des civilités
    data['name'] = data['name'].str.title()
    data['name'] = data['name'].str.strip()
    data['name'] = data['name'].str.replace(r'\b(Mr\.|Dr\.|Mrs\.|Ms\.)\s*', '', regex=True)
    # Arrondi des montants et décompte des valeurs négatives
    data['billing_amount'] = data['billing_amount'].round(2)
    if data[data['billing_amount'] < 0].shape[0] > 0:
        print(f"ATTENTION:Nombre de valeurs négatives dans 'billing_amount' : {data[data['billing_amount'] < 0].shape[0]}")
    else:
        print("Aucune valeur négative dans 'billing_amount'")
    # Normaliser les dates
    data['date_of_admission'] = pd.to_datetime(data['date_of_admission'], errors="coerce")
    data['discharge_date'] = pd.to_datetime(data['discharge_date'], errors="coerce")
    # Modification de l'ordre des colonnes
    data = data[["patient_id","name","age","gender","blood_type","medical_condition","date_of_admission","doctor","hospital","insurance_provider",
                 "billing_amount","room_number","admission_type","discharge_date","medication","test_results"]]
    return data

if __name__ == "__main__":
    # Charger les variables d'environnement
    load_dotenv()
    input_path = "./data/healthcare_dataset.csv"
    output_path = "./data/cleaned_healthcare_dataset.csv"
    try:
        print(f"Original data shape: {pd.read_csv(input_path).shape}")
        # Nettoyer les données et les sauvegarder dans un nouveau fichier CSV
        cleaned_data = clean_data(input_path)
        cleaned_data.to_csv(output_path, index=False)
        print(f"Cleaned data shape: {pd.read_csv(output_path).shape}")
        print(f"Data cleaned and saved to {output_path}")
    except Exception as e:
        print(f"Error during data cleaning: {e}")
        raise e

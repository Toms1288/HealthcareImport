import pandas as pd
import pymongo
import os
import numpy as np

data = pd.read_csv('healthcare_dataset.csv')




def clean_data(data):
    data = pd.read_csv('healthcare_dataset.csv')
    # Supprimer les doublons et les valeurs manquantes
    data = data.drop_duplicates()
    data = data.dropna()
    # Normaliser les noms et arrondir les montants
    data['Name'] = data['Name'].str.title()
    data['Name'] = data['Name'].str.strip()
    data['Billing Amount'] = data['Billing Amount'].round(2)
    return data

if __name__ == "__main__":
    file_path = os.getenv("INPUT_DATA_PATH")
    try:
        cleaned_data = clean_data(data)
        cleaned_data.to_csv(file_path, index=False)
        print(f"Data cleaned and saved to {file_path}")
    except Exception as e:
        print(f"Erreur lors du nettoyage des données : {e}")
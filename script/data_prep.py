import pandas as pd
import os
from dotenv import load_dotenv


def clean_data(file_path):
    data = pd.read_csv(file_path)
    # Supprimer les doublons et les valeurs manquantes
    data = data.drop_duplicates()
    data = data.dropna()
    # Normaliser les noms et arrondir les montants
    data['Name'] = data['Name'].str.title()
    data['Name'] = data['Name'].str.strip()
    data['Billing Amount'] = data['Billing Amount'].round(2)
    return data

if __name__ == "__main__":
    load_dotenv()
    input_path = os.environ.get("INPUT_DATA_PATH")
    output_path = os.environ.get("OUTPUT_DATA_PATH")
    try:
        print(pd.read_csv(input_path).shape)
        cleaned_data = clean_data(input_path)
        cleaned_data.to_csv(output_path, index=False)
        print(pd.read_csv(output_path).shape)
        print(f"Data cleaned and saved to {output_path}")
    except Exception as e:
        print(f"Erreur lors du nettoyage des données : {e}")

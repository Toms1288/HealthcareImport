import unittest
from pymongo import MongoClient
import pandas as pd
import numpy as np
from typing import List, Dict, Any
import os
from datetime import datetime
from bson import ObjectId, Decimal128

# --- CLASSE DE VALIDATION ---
class DataFrameValidator:
    REQUIRED_COLUMNS = [
        "patient_id", "name", "age", "gender", "blood_type",
        "medical_condition", "date_of_admission", "billing_amount",
        "discharge_date", "test_results"
    ]
    DATE_COLUMNS = ["date_of_admission", "discharge_date"]
    EXPECTED_TYPES = {
        "patient_id": "int64",
        "name": "str",
        "age": "int64",
        "gender": "str",
        "blood_type": "str",
        "medical_condition": "str",
        "date_of_admission": "datetime64[us]",
        "billing_amount": "float64",
        "discharge_date": "datetime64[us]",
        "test_results": "str"
    }

    @classmethod
    def validate(cls, df: pd.DataFrame) -> dict:
        """Retourne un dictionnaire avec le statut (PASS/FAIL) et les détails pour chaque validation."""
        results = {
            "required_columns": {"status": "PASS", "details": None},
            "missing_values": {"status": "PASS", "details": None},
            "duplicates": {"status": "PASS", "details": None},
            "data_types": {"status": "PASS", "details": None},
            "date_formats": {"status": "PASS", "details": None}
        }

        # 1. Colonnes obligatoires
        missing_columns = [col for col in cls.REQUIRED_COLUMNS if col not in df.columns]
        if missing_columns:
            results["required_columns"]["status"] = "FAIL"
            results["required_columns"]["details"] = f"Colonnes manquantes: {missing_columns}"
        else:
            results["required_columns"]["status"] = "PASS"
            results["required_columns"]["details"] = "Toutes les colonnes obligatoires sont présentes"
        # 2. Valeurs manquantes
        missing_values = df.isnull().sum()
        missing_values = missing_values[missing_values > 0]
        if missing_values.empty:
            results["missing_values"]["status"] = "PASS"
            results["missing_values"]["details"] = "Aucune valeur manquante trouvée"
        else:   
            results["missing_values"]["status"] = "FAIL"
            results["missing_values"]["details"] = f"Valeurs manquantes trouvées dans les colonnes: {missing_values.index.tolist()}"
        # 3. Doublons
        duplicates = df.duplicated().sum()
        if duplicates == 0:
            results["duplicates"]["status"] = "PASS"
            results["duplicates"]["details"] = "Aucun doublon trouvé"
        else:
            results["duplicates"]["status"] = "FAIL"
            results["duplicates"]["details"] = f"{duplicates} doublons trouvés"
        # 4. Types de données
        type_errors = {}
        for col, expected_type in cls.EXPECTED_TYPES.items():
            if col in df.columns and str(df[col].dtype) != expected_type:
                type_errors[col] = f"Attendu: {expected_type}, Obtenu: {df[col].dtype}"
        if type_errors:
            results["data_types"]["status"] = "FAIL"
            results["data_types"]["details"] = type_errors
        else:
            results["data_types"]["status"] = "PASS"
            results["data_types"]["details"] = "Tous les types de données sont corrects"
        # 5. Format des dates
        date_errors = {}
        for col in cls.DATE_COLUMNS:
            if col in df.columns:
                invalid_dates = []
                for idx, date_str in enumerate(df[col].dropna()):
                    try:
                        pd.to_datetime(date_str, format="mixed", errors="raise")
                    except (ValueError, TypeError):
                        invalid_dates.append((idx, date_str))
                if invalid_dates:
                    date_errors[col] = [f"Ligne {idx}: '{date}'" for idx, date in invalid_dates]
        if date_errors:
            results["date_formats"]["status"] = "FAIL"
            results["date_formats"]["details"] = date_errors
        else:
            results["date_formats"]["status"] = "PASS"
            results["date_formats"]["details"] = "Tous les formats de date sont corrects"

        return results

    @classmethod
    def print_validation_report(cls, results: dict) -> None:
        """Affiche un rapport de validation coloré."""
        print("\n--- 📋 Rapport de Validation ---")
        for check, result in results.items():
            status_icon = "✅" if result["status"] == "PASS" else "❌"
            print(f"{status_icon} **{check.replace('_', ' ').title()}**: {result['status']}")
            if result["details"]:
                print(f"   → {result['details']}")
        print("-------------------------------\n")

# --- TESTS UNITAIRES ---
class TestDataFrameValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
# Chemin vers le fichier CSV source
        cls.output_path = os.getenv("OUTPUT_DATA_PATH")
# Charger les données CSV
        cls.df = pd.read_csv(cls.output_path,parse_dates=['date_of_admission','discharge_date'])
        cls.validator = DataFrameValidator()

    def test_required_columns(self):
        results = self.validator.validate(self.df)
        self.assertEqual(results["required_columns"]["status"], "PASS",
                         f"Échec inattendu: {results['required_columns']['details']}")

    def test_missing_values(self):
        results = self.validator.validate(self.df)
        self.assertEqual(results["missing_values"]["status"], "PASS")
        self.assertEqual(results["missing_values"]["details"], "Aucune valeur manquante trouvée")

    def test_duplicates(self):
        df_with_duplicates = pd.concat([self.df, self.df.iloc[[0]]], ignore_index=True)
        results = self.validator.validate(df_with_duplicates)
        self.assertEqual(results["duplicates"]["status"], "FAIL")
        self.assertIn("1 doublons trouvés", results["duplicates"]["details"])

    def test_data_types(self):
        results = self.validator.validate(self.df)
        self.assertEqual(results["data_types"]["status"], "PASS")

    def test_date_formats(self):
        results = self.validator.validate(self.df)
        self.assertEqual(results["date_formats"]["status"], "PASS")
        self.assertEqual(results["date_formats"]["details"], "Tous les formats de date sont corrects")
        
if __name__ == '__main__':
    # Exécute les tests ET affiche le rapport pour le DataFrame de test
    df = pd.read_csv(os.getenv("OUTPUT_DATA_PATH"),parse_dates=['date_of_admission','discharge_date'])
    validator = DataFrameValidator()
    results = validator.validate(df)
    validator.print_validation_report(results)  # Affiche le rapport avant les tests
    unittest.main(verbosity=2)

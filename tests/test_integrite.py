import unittest
from pymongo import MongoClient
import pandas as pd
import numpy as np
import os
from datetime import datetime
from bson import ObjectId, Decimal128
from typing import Dict, Any
from dotenv import load_dotenv
load_dotenv()

class SingleCollectionIntegrityTest(unittest.TestCase):
    # 🔹 À adapter : Mapping des noms de colonnes CSV → MongoDB
    # Exemple : Si ton CSV a "Patient_ID" et MongoDB a "patientId"
    FIELD_MAPPING = {
        # 'Nom dans CSV': 'nomDansMongoDB'
        'patient_id': 'patient_id',
        'name': 'name',
        'age': 'age',
        'gender': 'gender',
        'blood_type': 'blood_type',
        'medical_condition': 'medical_condition',
        'date_of_admission': 'date_of_admission',
        'billing_amount': 'billing_amount',
        'discharge_date': 'discharge_date',
        'test_results': 'test_results'
    }

    def setUp(self):
        # CSV
        self.csv_path = os.getenv("OUTPUT_DATA_PATH")
        self.assertTrue(os.path.exists(self.csv_path), f"Fichier {self.csv_path} introuvable")
        self.df = pd.read_csv(self.csv_path,parse_dates=['date_of_admission','discharge_date'])

        # Connexion MongoDB
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client[os.getenv('MONGO_INITDB_DATABASE')]
        self.collection_name = os.getenv("COLLECTION")



    def tearDown(self):
        self.client.close()

    # --- Méthodes utilitaires ---
    def get_csv_schema(self) -> Dict[str, str]:
        """Retourne le schéma du CSV (noms des colonnes → types)."""
        schema = {}
        for col in self.df.columns:
            dtype = str(self.df[col].dtype)
            if 'int' in dtype:
                schema[col] = 'int'
            elif 'float' in dtype:
                schema[col] = 'float'
            elif 'datetime' in dtype:
                schema[col] = 'datetime'
            else:
                schema[col] = 'str'
        return schema

    def get_mongo_field_type(self, value: Any) -> str:
        """Retourne le type d'une valeur MongoDB."""
        if value is None:
            return 'null'
        elif isinstance(value, (dict, list)):
            return 'object'
        elif isinstance(value, bool):
            return 'bool'
        elif isinstance(value, int):
            return 'int'
        elif isinstance(value, (float, Decimal128)):
            return 'float'
        elif isinstance(value, datetime):
            return 'datetime'
        elif isinstance(value, str):
            return 'str'
        return type(value).__name__

    def get_mongo_schema(self) -> Dict[str, str]:
        """Retourne le schéma de la collection MongoDB."""
        schema = {}
        sample_doc = self.db[self.collection_name].find_one()
        if sample_doc:
            for field, value in sample_doc.items():
                if field != '_id':  # Ignore l'ID auto-généré
                    schema[field] = self.get_mongo_field_type(value)
        return schema

    def map_csv_to_mongo_field(self, csv_field: str) -> str:
        """Mappe un nom de colonne CSV vers son équivalent MongoDB."""
        return self.FIELD_MAPPING.get(csv_field, csv_field)  # Par défaut : même nom

    # --- Tests ---
    def test_collection_exists(self):
        """Vérifie que la collection existe."""
        collections = self.db.list_collection_names()
        self.assertIn(
            self.collection_name,
            collections,
            f"Collection '{self.collection_name}' introuvable dans la base"
        )

    def test_record_count(self):
        """Vérifie que le nombre d'enregistrements correspond entre CSV et MongoDB."""
        csv_count = len(self.df)
        mongo_count = self.db[self.collection_name].count_documents({})
        self.assertEqual(csv_count, mongo_count,
            f"Nombre d'enregistrements identiques entre CSV et MongoDB : CSV={csv_count}, MongoDB={mongo_count}"
        )

    def test_data_types(self):
        """Vérifie que les types de données sont cohérents."""
        csv_schema = self.get_csv_schema()
        mongo_schema = self.get_mongo_schema()

        for csv_field, csv_type in csv_schema.items():
            mongo_field = self.map_csv_to_mongo_field(csv_field)
            mongo_type = mongo_schema.get(mongo_field)

            if mongo_type is None:
                continue  # Champ absent dans MongoDB (optionnel : lever une erreur)

            # Compatibilité des types numériques
            if {csv_type, mongo_type} <= {'int', 'float'}:
                continue

            self.assertEqual(
                csv_type,
                mongo_type,
                f"Type incohérent pour '{csv_field}' (CSV: {csv_type}, MongoDB: {mongo_type})"
            )

if __name__ == '__main__':
    
    unittest.main(verbosity=2)
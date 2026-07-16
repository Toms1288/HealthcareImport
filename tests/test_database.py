import unittest
from pymongo import MongoClient
import pandas as pd
import numpy as np
from typing import List, Dict, Any
import os
from datetime import datetime
from bson import ObjectId, Decimal128

class DataIntegrityTest(unittest.TestCase):
    def setUp(self):
        # Chemin vers le fichier CSV source
        self.csv_path = os.getenv("OUTPUT_DATA_PATH")
        
        # Charger les données CSV
        self.df_source = pd.read_csv(self.csv_path)
        
        # Convertir les types de données pandas en types Python standards
        self.df_source = self.df_source.replace({np.nan: None})

    def tearDown(self):
        self.client_target.close()

    def get_csv_schema(self) -> Dict[str, Dict[str, str]]:
        """Extraire le schéma du DataFrame source selon notre structure"""
        schema = {
            'patient': {},
            'medical': {},
            'admission': {},
            'billing': {}
        }
        
        # Mapping des colonnes vers les collections
        mappings = {
            'patient': ['Name', 'Age', 'Gender', 'Blood Type'],
            'medical': ['Medical Condition', 'Medication', 'Test Results', 'Doctor'],
            'admission': ['Date of Admission', 'Discharge Date', 'Admission Type', 'Room Number', 'Hospital'],
            'billing': ['Insurance Provider', 'Billing Amount']
        }
        
        for collection, fields in mappings.items():
            for field in fields:
                if field in self.df_source.columns:
                    dtype = self.df_source[field].dtype
                    if pd.api.types.is_integer_dtype(dtype):
                        schema[collection][field] = 'int'
                    elif pd.api.types.is_float_dtype(dtype):
                        schema[collection][field] = 'float'
                    elif pd.api.types.is_datetime64_any_dtype(dtype):
                        schema[collection][field] = 'datetime'
                    else:
                        schema[collection][field] = 'str'
        
        return schema

    def get_mongo_schema(self) -> Dict[str, Dict[str, str]]:
        """Extraire le schéma des collections MongoDB"""
        schema = {}
        
        def extract_type(value):
            if value is None:
                return 'null'
            elif isinstance(value, dict):
                return 'object'
            elif isinstance(value, bool):
                return 'bool'
            elif isinstance(value, int):
                return 'int'
            elif isinstance(value, float) or isinstance(value, Decimal128):
                return 'float'
            elif isinstance(value, datetime):
                return 'datetime'
            elif isinstance(value, str):
                return 'str'
            return type(value).__name__
        
        for collection in self.collections:
            schema[collection] = {}
            sample_doc = self.db_target[collection].find_one()
            if sample_doc:
                for field, value in sample_doc.items():
                    if field not in ['_id', 'patientId']:
                        schema[collection][field] = extract_type(value)
        
        return schema

    def test_file_existence(self):
        """Vérifier que le fichier CSV existe"""
        self.assertTrue(
            os.path.exists(self.csv_path),
            f"Le fichier CSV {self.csv_path} n'existe pas"
        )

    def test_collection_presence(self):
        """Vérifier que toutes les collections existent"""
        db_collections = self.db_target.list_collection_names()
        for collection in self.collections:
            self.assertIn(
                collection,
                db_collections,
                f"La collection {collection} n'existe pas dans MongoDB"
            )

    def test_data_types(self):
        """Vérifier que les types de données sont cohérents"""
        csv_schema = self.get_csv_schema()
        mongo_schema = self.get_mongo_schema()
        
        for collection in self.collections:
            for field in csv_schema[collection]:
                csv_type = csv_schema[collection][field]
                mongo_type = mongo_schema[collection].get(field)
                
                # Mapping des noms de colonnes CSV vers MongoDB
                field_mapping = {
                    'Name': 'name',
                    'Age': 'age',
                    'Gender': 'gender',
                    'Blood Type': 'bloodType',
                    'Medical Condition': 'condition',
                    'Test Results': 'testResults',
                    'Insurance Provider': 'insuranceProvider',
                    'Billing Amount': 'amount'
                }
                
                mongo_field = field_mapping.get(field, field.lower())
                mongo_type = mongo_schema[collection].get(mongo_field)
                
                if mongo_type:
                    # Vérification de compatibilité des types
                    if csv_type in ['int', 'float'] and mongo_type in ['int', 'float']:
                        continue
                    
                    self.assertEqual(
                        csv_type,
                        mongo_type,
                        f"Le type du champ {field} ne correspond pas dans la collection {collection}"
                    )

    def test_record_count(self):
        """Vérifier que le nombre d'enregistrements est cohérent"""
        csv_count = len(self.df_source)
        
        for collection in self.collections:
            mongo_count = self.db_target[collection].count_documents({})
            self.assertEqual(
                csv_count,
                mongo_count,
                f"Le nombre d'enregistrements ne correspond pas pour la collection {collection}"
            )

    def test_relationships(self):
        """Vérifier l'intégrité des relations entre les collections"""
        # Récupérer tous les IDs de patients
        patient_ids = set(str(doc['_id']) for doc in self.db_target['patient'].find({}, {'_id': 1}))
        
        for collection in ['medical', 'admission', 'billing']:
            related_ids = set(str(doc['patientId']) for doc in self.db_target[collection].find({}, {'patientId': 1}))
            
            # Vérifier que chaque patientId existe dans la collection patient
            self.assertEqual(
                patient_ids,
                related_ids,
                f"Les relations patientId ne correspondent pas dans la collection {collection}"
            )

    def test_null_values(self):
        """Vérifier les valeurs nulles pour chaque collection"""
        def count_csv_nulls(df, fields):
            return df[fields].isnull().sum().to_dict()

        def count_mongo_nulls(collection, fields):
            null_counts = {}
            for field in fields:
                null_count = self.db_target[collection].count_documents({field: None})
                null_counts[field] = null_count
            return null_counts

        # Mapping des champs pour chaque collection
        field_mappings = {
            'patient': {
                'csv': ['Name', 'Age', 'Gender', 'Blood Type'],
                'mongo': ['name', 'age', 'gender', 'bloodType']
            },
            'medical': {
                'csv': ['Medical Condition', 'Medication', 'Test Results', 'Doctor'],
                'mongo': ['condition', 'medication', 'testResults', 'doctor']
            },
            'admission': {
                'csv': ['Date of Admission', 'Discharge Date', 'Admission Type', 'Room Number', 'Hospital'],
                'mongo': ['dateOfAdmission', 'dischargeDate', 'admissionType', 'roomNumber', 'hospital']
            },
            'billing': {
                'csv': ['Insurance Provider', 'Billing Amount'],
                'mongo': ['insuranceProvider', 'amount']
            }
        }

        for collection, fields in field_mappings.items():
            csv_nulls = count_csv_nulls(self.df_source, fields['csv'])
            mongo_nulls = count_mongo_nulls(collection, fields['mongo'])
            
            # Comparer les valeurs nulles en tenant compte du mapping des noms de champs
            for csv_field, mongo_field in zip(fields['csv'], fields['mongo']):
                self.assertEqual(
                    csv_nulls[csv_field],
                    mongo_nulls[mongo_field],
                    f"Le nombre de valeurs nulles ne correspond pas pour le champ {csv_field} dans la collection {collection}"
                )

if __name__ == '__main__':
    unittest.main()
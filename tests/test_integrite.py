from pymongo import MongoClient
import os
import unittest
from typing import Dict
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

class TestIntegrite(unittest.TestCase):
    def setUpClass(cls):
        """Configuration initiale pour la classe de test"""
        cls.client = MongoClient(os.getenv('MONGODB_URI'))
        cls.db = cls.client.test_database
        cls.collection = cls.db.test_collection
        
    def test_collection_presence(self):
        """Vérifier que toutes les collections existent"""
        db_collections = self.db_target.list_collection_names()
        for collection in self.collections:
            self.assertIn(
                collection,
                db_collections,
                f"La collection {collection} n'existe pas dans MongoDB"
            )
            
    def test_record_count(self):
        """Vérifier que le nombre d'enregistrements est cohérent"""
        csv_count = len(self.output_df)
        
        for collection in self.collections:
            mongo_count = self.db_target[collection].count_documents({})
            self.assertEqual(
                csv_count,
                mongo_count,
                f"Le nombre d'enregistrements ne correspond pas pour la collection {collection}"
            )


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
    
    def tearDownClass(cls):
        """Nettoyage après tous les tests"""
        # cls.client.drop_database("test_database")
        cls.client.close()


if __name__ == '__main__':
    unittest.main()
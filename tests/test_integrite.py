from pymongo import MongoClient
import os
import unittest
from typing import Dict
from datetime import datetime
import pandas as pd
import numpy as np
from dotenv import load_dotenv
load_dotenv()

class TestIntegrite(unittest.TestCase):
    def setUp(self):
        # Chemin vers le fichier CSV source
        self.csv_path = os.getenv("OUTPUT_DATA_PATH")
        
        # Connexion à la base MongoDB cible
        self.client_target = MongoClient(os.getenv('MONGODB_URI'))
        self.db_target = self.client_target[os.getenv('MONGO_INITDB_DATABASE')]
        
        # Collection MongoDB
        self.collection = ['HealthcareData']
        
        # Charger les données CSV
        self.df_source = pd.read_csv(self.csv_path)
        
        # Convertir les types de données pandas en types Python standards
        self.df_source = self.df_source.replace({np.nan: None})
    def test_collection_presence(self):
        """Vérifier que toutes les collections existent"""
        db_collections = self.db_target.list_collection_names()
        for collection in self.collection:
            self.assertIn(
                collection,
                db_collections,
                f"La collection {collection} n'existe pas dans MongoDB"
            )
            
    def test_record_count(self):
        """Vérifier que le nombre d'enregistrements est cohérent"""
        csv_count = len(self.df_source)
        mongo_count = self.db_target[self.collection[0]].count_documents({})
        self.assertEqual(
            csv_count,
            mongo_count,
            f"Le nombre d'enregistrements ne correspond pas pour la collection {self.collection[0]}"
        )



if __name__ == '__main__':
    unittest.main()
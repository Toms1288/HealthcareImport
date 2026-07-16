from pymongo import MongoClient
import os
import unittest

from dotenv import load_dotenv
load_dotenv()

class TestIntegrite(unittest.TestCase):
    def setUpClass(cls):
        """Configuration initiale pour la classe de test"""
        cls.client = MongoClient(os.getenv('MONGODB_URI'))
        cls.db = cls.client.test_database
        cls.collection = cls.db.test_collection

    def setUp(self):
        """Nettoie la collection avant chaque test"""
        self.collection.delete_many({})

    def test_insert_and_find(self):
        """Test d'insertion et de recherche"""
        test_data = {"name": "test", "value": 123}
        result = self.collection.insert_one(test_data)
        self.assertTrue(result.inserted_id is not None)
        found = self.collection.find_one({"name": "test"})
        self.assertIsNotNone(found)
        self.assertEqual(found["value"], 123)

    def test_delete(self):
        """Test de suppression"""
        test_data = [
            {"name": "test1", "value": 111},
            {"name": "test2", "value": 222},
            {"name": "test3", "value": 333}
        ]

        self.collection.insert_many(test_data)
        initial_count = self.collection.count_documents({})
        delete_result = self.collection.delete_one({"name": "test1"})
        self.assertEqual(delete_result.deleted_count, 1)
        self.assertEqual(self.collection.count_documents({}), initial_count - 1)
        self.assertIsNone(self.collection.find_one({"name": "test1"}))

    def tearDownClass(cls):
        """Nettoyage après tous les tests"""
        # cls.client.drop_database("test_database")
        cls.client.close()


if __name__ == '__main__':
    unittest.main()
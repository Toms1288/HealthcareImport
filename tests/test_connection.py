from pymongo import MongoClient, errors
import os
import unittest
from dotenv import load_dotenv
load_dotenv()


class TestConnection(unittest.TestCase):
    def setUp(self):
            """Configuration initiale avant chaque test"""
            self.uri = os.getenv('MONGODB_URI')
            self.db_name = os.getenv('MONGO_INITDB_DATABASE')

            
    def test_connection(self):
        """Test d'une connexion à MongoDB"""
        try:
            # Tentative de connexion
            client = MongoClient(self.uri, serverSelectionTimeoutMS=1000)  # Timeout de 1 seconde

            # Force une connexion en exécutant une commande
            client.admin.command('ping')

            # Si on arrive ici, la connexion est réussie
            self.assertTrue(True)
            print("Connexion à MongoDB réussie")
            
        except errors.ConnectionFailure:
            self.fail("La connexion à MongoDB a échoué")
            
        finally:
            if 'client' in locals():
                client.close()
                
    def test_connection_invalid_uri(self):
        """Test d'une connexion avec une URI invalide"""
        invalid_uri = "mongodb://invalid_user:invalid_pass@localhost:27017"
        with self.assertRaises(errors.ConfigurationError):
            MongoClient(invalid_uri, serverSelectionTimeoutMS=1000)
            print("Connexion avec URI invalide échouée comme prévu")

            
    def test_database_CRUD(self):
        """Test de création, de lecture, de mise à jour et de suppression dans une base de données"""
        try:
            client = MongoClient(self.uri)
            db = client[self.db_name]
            
            # Création d'une collection pour tester
            collection = db.test_collection
            print(f"Collection créée: {collection.name}")
            result = collection.insert_one({"test": "data"})
            print(f"Document inséré avec succès: {result.inserted_id}")
            
            # Vérification que l'insertion a fonctionné
            self.assertTrue(result.inserted_id is not None)
            
            # Test de lecture
            found = collection.find_one({"test": "data"})
            self.assertIsNotNone(found)
            self.assertEqual(found["test"], "data")
            print(f"Document trouvé: {found}")
            
            # Test de mise à jour
            collection.update_one({"test": "data"}, {"$set": {"test": "updated_data"}})
            updated = collection.find_one({"test": "updated_data"})
            self.assertIsNotNone(updated)
            print(f"Document mis à jour: {updated}")
            
            # Test de suppression
            collection.delete_one({"test": "updated_data"})
            deleted = collection.find_one({"test": "updated_data"})
            self.assertIsNone(deleted)
            print("Document supprimé avec succès")
            
        finally:
            if 'client' in locals():
                collection.drop()  # Nettoyer la collection de test
                client.close()


if __name__ == '__main__':
    unittest.main()
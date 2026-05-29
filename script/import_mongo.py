
import pandas as pd
import pymongo
import os
from dotenv import load_dotenv  




def import_to_mongodb(file_path, mongodb_uri, db_name, collection_name):
    # Lire le fichier CSV
    df = pd.read_csv(file_path)
    #Connecter à MongoDB et créer la base de données et la collection
    client = pymongo.MongoClient(mongodb_uri)
    # Sélectionner la base de données
    db = client[db_name]
    
    # Diviser le DataFrame en blocs de 1000 lignes
    chunk_size = 1000
    num_chunks = int((len(df))/chunk_size)+1
    chunks = []
    
    
    # Créer les blocs de données   
    for i in range(num_chunks):
        start = chunk_size * i
        stop = start + chunk_size
        chunks.append(df[start:stop])
    # Itérer sur les blocs pour les insérer dans MongoDB    
    for i in range(num_chunks):
        db[collection_name].insert_many(chunks[i].to_dict('records'))
        print(f"Chunk {i+1}/{num_chunks} imported successfully.")
    # Compter le nombre total de documents
    count = db[collection_name].count_documents({})
    print(f"Total documents in collection: {count}")
    
if __name__ == "__main__":
    # Charger les variables d'environnement
    load_dotenv()
    file_path = os.environ.get("OUTPUT_DATA_PATH")
    db_name = os.environ.get("MONGO_INITDB_DATABASE")
    collection_name = os.environ.get("COLLECTION")
    user = os.environ.get("MONGO_ADMIN_USERNAME")
    password = os.environ.get("MONGO_ADMIN_PASSWORD")
    mongodb_uri = os.environ.get("MONGODB_URI")
    # Lancement l'importation des données dans MongoDB
    try:
        import_to_mongodb(file_path, mongodb_uri, db_name, collection_name)
        print("Data imported successfully.")
    except Exception as e:
        print(f"Error during import: {e}")

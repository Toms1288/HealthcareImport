import math
import pandas as pd
import pymongo
from pymongo.errors import BulkWriteError
import os
from dotenv import load_dotenv  

def import_to_mongodb(file_path, mongodb_uri, db_name, collection_name):
    # Lire le fichier CSV
    df = pd.read_csv(file_path,parse_dates=['date_of_admission','discharge_date'])
    #Connecter à MongoDB et créer la base de données et la collection
    client = pymongo.MongoClient(mongodb_uri)
    # Sélectionner la base de données
    db = client[db_name]
    # Sélectionner la collection et créer un index unique sur le champ "patient_id"
    collection = db[collection_name]
    collection.create_index("patient_id", unique=True)
    
    
    # Diviser le DataFrame en blocs de 1000 lignes
    chunk_size = 1000
    num_chunks = math.ceil((len(df) / chunk_size))
    chunks = []
    # Compter le nombre total de documents avant l'importation
    count = db[collection_name].count_documents({})
    print(f"Total documents in collection avant l'import: {count}")    
    
    # Créer les blocs de données   
    for i in range(num_chunks):
        start = chunk_size * i
        stop = start + chunk_size
        chunks.append(df[start:stop])
    # Itérer sur les blocs pour les insérer dans MongoDB    
    for i in range(num_chunks):
        # Vérification des doublons avant l'insertion
        existing_patients = collection.distinct("patient_id")
        new_records = [r for r in chunks[i].to_dict('records') if r["patient_id"] not in existing_patients]
        if new_records==[]:
            print(f"Chunk {i+1}/{num_chunks} has no new records to import.")
            continue
        try:
            collection.insert_many(new_records, ordered=False)
            print(f"Chunk {i+1}/{num_chunks} imported successfully.")
        except BulkWriteError as bwe:
                print(f"Chunk {i+1}/{num_chunks} import encountered errors: {bwe.details}")

    # Compter le nombre total de documents après l'importation
    count = db[collection_name].count_documents({})
    print(f"Total documents in collection après l'import: {count}")
    
if __name__ == "__main__":
    # Charger les variables d'environnement
    load_dotenv()
    file_path = os.environ.get("OUTPUT_DATA_PATH")
    db_name = os.environ.get("MONGO_INITDB_DATABASE")
    collection_name = os.environ.get("COLLECTION")
    user = os.environ.get("MONGO_APP_USERNAME")
    password = os.environ.get("MONGO_APP_PASSWORD")
    mongodb_uri = os.environ.get("MONGODB_URI")
    # Lancement l'importation des données dans MongoDB
    try:
        import_to_mongodb(file_path, mongodb_uri, db_name, collection_name)
        print("Data imported successfully.")
    except Exception as e:
        print(f"Error during import: {e}")
        raise e

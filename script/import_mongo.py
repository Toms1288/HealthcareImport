
import pandas as pd
import pymongo
import os
from dotenv import load_dotenv  




def import_to_mongodb(file_path, mongodb_uri, db_name, collection_name):
    
    df = pd.read_csv(file_path)
    #Connecter à MongoDB et créer la base de données et la collection
    client = pymongo.MongoClient(mongodb_uri, 'mongodb://mongodb:27017')
    
    db = client[db_name]
    
    
    chunk_size = 1000
    num_chunks = int((len(df))/chunk_size)+1
    chunks = []
    
    
        
    for i in range(num_chunks):
        start = chunk_size * i
        stop = start + chunk_size
        chunks.append(df[start:stop])
    # itérer sur les blocs    
    for i in range(num_chunks):
        db[collection_name].insert_many(chunks[i].to_dict('records'))
        print(f"Chunk {i+1}/{num_chunks} imported successfully.")
        
    count = db[collection_name].count_documents({})
    print(f"Total documents in collection: {count}")
    
if __name__ == "__main__":
    load_dotenv()
    file_path = os.environ.get("OUTPUT_DATA_PATH")
    db_name = os.environ.get("MONGO_INITDB_DATABASE")
    collection_name = os.environ.get("COLLECTION")
    user = os.environ.get("MONGO_APP_USER")
    password = os.environ.get("MONGO_APP_PASSWORD")
    mongodb_uri = f"mongodb://${user}:${password}@mongodb:27017/{db_name}?authSource=$admin"

    try:
        import_to_mongodb(file_path, mongodb_uri, db_name, collection_name)

    except Exception as e:
        print(f"Erreur lors de l'insertion : {e}")

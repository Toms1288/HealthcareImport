import pandas as pd
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

file_path = os.environ.get("OUTPUT_DATA_PATH")
mongodb_uri = os.environ.get("MONGODB_URI")
db_name = os.environ.get("MONGO_INITDB_DATABASE")
collection_name = os.environ.get("COLLECTION")
user = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
password = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")
mongodb_url = f'mongodb://{user}:{password}@localhost:27017/{db_name}'
print(mongodb_url)
    
df = pd.read_csv(file_path)
    #Connecter à MongoDB et créer la base de données et la collection
client = pymongo.MongoClient(mongodb_uri)
db = client[db_name]
    
    
chunk_size = 1000
num_chunks = int((len(df))/chunk_size)
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
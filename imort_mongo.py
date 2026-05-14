import pandas as pd
import pymongo
import os
import numpy as np

data = pd.read_csv('healthcare_dataset.csv')






def clean_data(data):
    # Supprimer les doublons
    data = data.drop_duplicates()
    data = data.dropna()
    data['Name'] = data['Name'].str.title()
    data['Name'] = data['Name'].str.strip()
    data['Billing Amount'] = data['Billing Amount'].round(2)
    return data



def import_to_mongodb(data):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['DataSoluTech']
    
    
    chunk_size = 1000
    num_chunks = int((len(data))/chunk_size)
    chunks = []
        
    for i in range(num_chunks):
        start = chunk_size * i
        stop = start + chunk_size
        chunks.append(data[start:stop])
    # itérer sur les blocs    
    for i in range(num_chunks):
        db.healthcare.insert_many(chunks[i].to_dict('records'))
        print(f"Chunk {i+1}/{num_chunks} imported successfully.")
    
if __name__ == "__main__":
    cleaned_data = clean_data(data)
    import_to_mongodb(cleaned_data) 
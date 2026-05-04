import kagglehub
import pandas as pd
import pymongo

# Download latest version
path = kagglehub.dataset_download("prasad22/healthcare-dataset")

data = pd.read_csv('file:///C:/Users/Thomas%20LECLERCQ/.cache/kagglehub/datasets/prasad22/healthcare-dataset/versions/2/healthcare_dataset.csv')



client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['DataSoluTech']
db.healthcare.insert_many(data.to_dict('records'))
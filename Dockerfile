FROM python:3

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY script /app/script
COPY database /app/data

CMD ["bash", "-c", "python script/data_prep.py && python script/import_mongo.py"]

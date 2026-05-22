FROM python:3

WORKDIR /usr/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY script/ /app/script/

CMD ["bash", "-c", "python script/data_prep.py && python script/import_mongo.py"]

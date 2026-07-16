FROM python:3

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY scripts /app/scripts
COPY data /app/data
COPY tests /app/tests

CMD ["bash", "-c", "python tests/test_connection.py && python scripts/data_prep.py && python tests/test_database.py && python scripts/import_mongo.py && python tests/test_integrite.py"]

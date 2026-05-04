FROM python:3.12-slim

WORKDIR /script

COPY requirements.txt requirements.txt

RUN pip install -r requirement.txt

COPY . .

EXPOSE 27017


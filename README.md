# Import d'une  base de donnée dans MongoDB par une  application Python grace à Docker

Application de traitement de données utilisant MongoDB dans un conteneur Docker, 
accompagnée de tests unitaires en Python avec pymongo,
elle importe les données qui sont dans un fichier en format csv dans une collection de la base de données NoSQL Mongodb(service dans un container Docker) 
et puis extraire les données qui se trouve dans la collection dans un fichier en formation json.

## Fonctionnalités

Configuration MongoDB via Docker-compose
Import de données CSV vers JSON

Tests unitaires pour:
- Connexion à MongoDB
- Opérations CRUD
- Intégrité des données

Export des données au format JSON

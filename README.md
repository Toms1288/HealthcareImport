# Projet 5 - Healthcare Data Pipeline

Application Docker pour nettoyer, traiter et importer des données de santé dans MongoDB.

## 🚀 Démarrage rapide

### Prérequis
- Docker et Docker Compose
- MongoDB Compass (optionnel, pour visualiser les données)
- Fichier `healthcare_dataset.csv` dans le dossier `./data/`

### Installation et lancement

```bash
# Naviguer vers le projet
cd "Projet 5"

# Démarrer les conteneurs (première fois)
docker compose up --build

# Démarrer les conteneurs (fois suivantes)
docker compose up

# Ou en arrière-plan
docker compose up -d
```

Les services démarreront automatiquement :
- **MongoDB** : `localhost:27017`
- **Python Service** : Traite et importe les données

## 📋 Architecture

### Services

#### MongoDB (`mongo:latest`)
- **Port** : `0.0.0.0:27017` (accessible depuis l'hôte et le réseau Docker)
- **Base de données** : `DataSoluTech`
- **Collection** : `Healthcare`
- **Authentification** : 
  - Admin : `root` / `root` (authSource: `admin`)
  - App : `user` / `user` (authSource: `DataSoluTech`)
- **Redémarrage** : Automatique (`always`)
- **Initialisation** : Script `mongo-init.js`
- **Healthcheck** : Ping MongoDB toutes les 10s (5s timeout, 5 retries)

#### Python Service (Image custom)
- **Build** : Basée sur le `Dockerfile` du projet
- **Fonction** : Nettoie les données CSV et importe dans MongoDB
- **Dépendances** : pandas, pymongo, python-dotenv
- **Dépend de** : Service MongoDB (attend son démarrage et sa bonne santé)
- **Healthcheck** : Ping sur endpoint `/health` toutes les 30s

### Volumes

| Volume | Source | Destination | Fonction |
|--------|--------|-------------|----------|
| `mongodb_data` | Volume Docker | `/data/db` | Données persistantes MongoDB |
| `./data` | Local | `/app/database` | Données CSV (input/output) |
| `./script` | Local | `/app/script` | Scripts Python |
| `./mongo-init.js` | Local | `/docker-entrypoint-initdb.d/` | Initialisation MongoDB |

### Réseau Docker

- **Nom** : `app_network`
- **Driver** : `bridge`
- **Fonction** : Communication inter-conteneurs
- **Service discovery** : Les conteneurs se trouvent par leur nom (`mongodb`, `python_service`)

## 🔐 Authentification MongoDB

### Identifiants

```env
# Admin (pour gérer la base)
Username: root
Password: root
Database: admin

# Application (pour l'import de données)
Username: user
Password: user
Database: DataSoluTech
```

### Initialisation

Au premier démarrage, le script `mongo-init.js` :
1. Crée un utilisateur administrateur dans la base `admin`
2. Crée un utilisateur applicatif dans la base `DataSoluTech`
3. Crée la collection `Healthcare` avec validation de schéma JSON

## 📊 Données

### Format d'entrée
- **Fichier** : `healthcare_dataset.csv`
- **Emplacement** : `./data/healthcare_dataset.csv`
- **Champs requis** :
  - `patient_id` : Identifiant unique du patient
  - `name` : Nom du patient
  - `age` : Âge (entier 0-150)
  - `gender` : Sexe (Male, Female, Other)
  - `blood_type` : Groupe sanguin (A+, A-, B+, B-, AB+, AB-, O+, O-)
  - `date_of_admission` : Date d'admission
  - `hospital` : Nom de l'hôpital
  - `discharge_date` : Date de sortie (optionnel)

### Traitement
- Les données brutes sont nettoyées
- Fichier nettoyé : `cleaned_healthcare_dataset.csv`
- Import par chunks de 1000 documents
- Destination : `DataSoluTech.Healthcare`

## 🛠️ Commandes utiles

### Healthchecks

```bash
# Vérifier le statut de santé des services
docker compose ps

# Voir le détail du healthcheck de MongoDB
docker inspect projet_5-mongodb-1 --format='{{.State.Health.Status}}'

# Voir le détail du healthcheck du service Python
docker inspect projet_5-python_service-1 --format='{{.State.Health.Status}}'

# Logs complets d'un service
docker compose logs mongodb
docker compose logs python_service
```

### Gestion des conteneurs

```bash
# Démarrer les services
docker compose up -d

# Arrêter les services
docker compose down

# Arrêter et supprimer les volumes (réinitialise la base de données)
docker compose down -v

# Reconstruire les images
docker compose build --no-cache

# Redémarrer un service
docker compose restart mongodb
docker compose restart python_service

# Voir le statut
docker compose ps
```

### Logs

```bash
# Logs de MongoDB
docker compose logs mongodb

# Logs du service Python
docker compose logs python_service

# Logs en temps réel
docker compose logs -f mongodb
docker compose logs -f python_service

# Logs avec limite
docker compose logs --tail=50 mongodb
```

### Accès direct à MongoDB

```bash
# Accéder à MongoDB Shell (mongosh)
docker compose exec mongodb mongosh -u root -p root --authenticationDatabase admin

# Dans mongosh - Commandes utiles
> show dbs                              # Lister les bases
> use DataSoluTech                      # Utiliser la base
> show collections                     # Lister les collections
> db.Healthcare.countDocuments()        # Compter les documents
> db.Healthcare.findOne()               # Voir un document
> db.Healthcare.find().limit(5)         # Voir 5 documents
> db.Healthcare.find({gender: "Male"})  # Filtrer par genre
> exit                                  # Quitter

# Sans entrer dans mongosh
docker compose exec mongodb mongosh -u root -p root --authenticationDatabase admin --eval "db.DataSoluTech.Healthcare.countDocuments()"
```

### Exécuter le script Python

```bash
# Relancer le service Python (exécute le script)
docker compose up python_service

# Ou en arrière-plan
docker compose up -d python_service

# Voir les logs d'exécution
docker compose logs -f python_service
```

## 🔗 Connexion MongoDB Compass

### Méthode 1 : Connection String

Collez cette chaîne dans MongoDB Compass :
```
mongodb://localhost:27017/
```

Ou pour accéder à la base applicative :
```
mongodb://user:user@localhost:27017/DataSoluTech?authSource=DataSoluTech
```

### Méthode 2 : Formulaire

| Paramètre | Admin | App |
|-----------|-------|-----|
| **Host** | localhost | localhost |
| **Port** | 27017 | 27017 |
| **Username** | root | user |
| **Password** | root | user |
| **Auth Database** | admin | DataSoluTech |

## 📁 Structure du projet

```
Projet 5/
├── docker-compose.yml              # Configuration Docker Compose (services, volumes, réseau)
├── Dockerfile                      # Image Python (installation des dépendances)
├── .env                            # Variables d'environnement
├── mongo-init.js                   # Script d'initialisation MongoDB (utilisateurs, schéma)
├── README.md                       # Documentation
├── scripts/
    ├── data_prep.py                # Script Python de néttoyage et préparation des données
│   └── import_mongodb.py           # Script d'import des données CSV dans MongoDB
└── data/
    ├── healthcare_dataset.csv      # Données brutes (input) ← À fournir
    └── cleaned_healthcare_dataset.csv # Données nettoyées (généré)
```

## 🐛 Dépannage

### Healthchecks en erreur

**MongoDB healthcheck échoue** :
```bash
# Vérifier qu'il écoute correctement
docker compose exec mongodb mongosh -u root -p root --authenticationDatabase admin --eval "db.adminCommand('ping')"

# Si échec, redémarrer
docker compose restart mongodb
```

**Python healthcheck échoue** :
- Vérifier que votre app Python a un endpoint `/health`
- Si l'app n'expose pas d'endpoint, modifier le healthcheck du docker-compose pour tester avec `python -c "print('healthy')"`
- Vérifier les logs : `docker compose logs python_service`

### Erreur : "Connection refused" (python_service)

**Cause** : Python tente de se connecter à MongoDB avant qu'il ne soit prêt

**Solution** :
```bash
# Option 1 : Attendre et relancer
docker compose restart python_service

# Option 2 : Augmenter le délai dans import_to_mongodb.py
# Ajouter un sleep au début du script
import time
time.sleep(5)
```

### Erreur : "Authentication failed"

**Cause** : Mauvais identifiants ou base d'authentification incorrecte

**Solution** :
```bash
# Réinitialiser la base
docker compose down -v
docker compose up --build

# Vérifier les identifiants
cat .env | grep MONGO
```

### Erreur : "Name or service not known"

**Cause** : DNS n'a pas résolu le nom du service

**Solutions** :
- Vérifier que les deux services sont sur le même réseau : `docker network inspect app_network`
- Redémarrer Docker Compose : `docker compose restart`
- Utiliser l'adresse IP locale si problème persiste

### Erreur : "ENOENT" ou "File not found"

**Cause** : Fichier `healthcare_dataset.csv` manquant

**Solution** :
```bash
# Créer le dossier data
mkdir data

# Copier le fichier CSV
cp healthcare_dataset.csv ./data/

# Vérifier
ls -la ./data/
```

### MongoDB n'écoute pas sur 0.0.0.0

**Vérifier** :
```bash
docker logs mongodb | grep "Listening on"
```

Devrait afficher :
```
Listening on 0.0.0.0:27017
```

Si affiche `127.0.0.1:27017`, c'est un problème de `bindIp`. Redémarrer avec :
```bash
docker compose down -v
docker compose up --build
```

## 📊 Schéma de données MongoDB

### Collection : Healthcare

```javascript
db.Healthcare.insertOne({
  _id: ObjectId(),
  patient_id: "P001",
  name: "Jean Dupont",
  age: 45,
  gender: "Male",
  blood_type: "O+",
  medical_condition: "Obesity",
  date_of_admission: ISODate("2026-05-27"),
  doctor: "Samantha Davies",  
  hospital: "Hôpital Central",
  insurance_provider: "Medicare",
  billing_amount: 33643.33,
  room_number: 352,
  admission_type: "Emergency",
  discharge_date: ISODate("2026-06-10"),
  medication: "Ibuprofen",
  test_results: "Inconclusive",
})
```

### Validation de schéma JSON

Tous les documents doivent respecter :
- Champs requis : `_id`, `patient_id`, `name`, `age`, `gender`, `blood_type`, `date_of_admission`, `hospital`,
- Âge : entier entre 0 et 150
- Sexe : "Male", "Female" ou "Other"
- Groupe sanguin : un des 8 types valides
- Dates : format ISO 8601
- Test Results : "Normal", "Abnormal" ou " Inconclusive"

## ✅ Checklist de démarrage

- [ ] Docker et Docker Compose installés et fonctionnels
- [ ] Fichier `healthcare_dataset.csv` dans `./data/`
- [ ] Fichier `.env` présent avec bonnes variables
- [ ] Dossier `./scripts/` avec `import_to_mongodb.py`
- [ ] Fichier `mongo-init.js` présent
- [ ] `docker compose up --build` réussi
- [ ] Pas d'erreur dans les logs : `docker compose logs`
- [ ] MongoDB accessible : `docker compose exec mongodb mongosh -u root -p root`
- [ ] Données importées : `db.Healthcare.countDocuments()`
- [ ] MongoDB Compass connecté avec succès

## 📝 Notes importantes

- **Données persistantes** : Stockées dans le volume `mongodb_data` (survit aux redémarrages)
- **Initialisation** : Le script `mongo-init.js` s'exécute une seule fois au premier démarrage
- **Pour réinitialiser** : `docker compose down -v` puis `docker compose up --build`
- **Port MongoDB** : Accessible depuis l'hôte (`localhost:27017`) ET depuis le réseau Docker (`mongodb:27017`)
- **Réseau** : Les deux services communiquent via le réseau `app_network` (bridge)
- **Import** : Se fait par chunks de 1000 documents (optimisation mémoire)

## 🔗 Ressources utiles

- [MongoDB Documentation](https://docs.mongodb.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [MongoDB Compass](https://www.mongodb.com/products/compass)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [Mongosh Manual](https://docs.mongodb.com/mongosh/current/)

## 👤 Auteur

Thomas LECLERCQ

---

**Dernière mise à jour** : 12/07/2026

**Changements récents** :
- Ajout des healthchecks Docker Compose (MongoDB et Python)
- Mélioration de la surveillance de l'état des services

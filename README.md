# Healthcare Data Pipeline

Application Docker complète pour nettoyer, traiter et importer des données de santé dans MongoDB avec validation de schéma et tests d'intégrité.

---

## 📋 Table des matières

1. [Prérequis](#-prérequis)
2. [Structure du projet](#-structure-du-projet)
3. [Variables d'environnement](#-variables-denvironnement)
4. [Installation et lancement](#-installation-et-lancement)
5. [Architecture](#-architecture)
6. [Schéma de la base](#-schéma-de-la-base)
7. [Index](#-index)
8. [Utilisateurs et rôles](#-utilisateurs-et-rôles)
9. [Nettoyage et migration](#-nettoyage-et-migration)
10. [Tests réalisés](#-tests-réalisés)
11. [Résultats attendus](#-résultats-attendus)
12. [Erreurs et solutions](#-erreurs-et-solutions)
13. [Commandes utiles](#-commandes-utiles)
14. [Ressources](#-ressources)

---

## 🔧 Prérequis

### Système
- **Système d'exploitation** : Linux, macOS, ou Windows 10+ (avec WSL2)
- **Espace disque** : Minimum 2 GB pour les images Docker et les données
- **Mémoire RAM** : Minimum 4 GB (recommandé 8 GB)
- **Connexion Internet** : Pour télécharger les images Docker

### Logiciels requis
| Logiciel | Version minimale | Version testée | Statut |
|----------|-----------------|----------------|--------|
| Docker | 20.10 | 27.x | ✅ Requis |
| Docker Compose | 1.29 | 2.x | ✅ Requis |
| Python | 3.10 | 3.12+ | 📦 Dans le conteneur |
| MongoDB Client (optionnel) | 5.0 | 7.x | ⚙️ Optionnel |
| MongoDB Compass (optionnel) | - | Latest | ⚙️ Recommandé |

### Vérification des installations

```bash
# Vérifier Docker
docker --version

# Vérifier Docker Compose
docker compose version

# Vérifier que le démon Docker tourne
docker ps
```

---

## 📁 Structure du projet

```
HealthcareImport-2/
├── 📄 docker-compose.yml           # Configuration orchestration services
├── 📄 Dockerfile                   # Image Docker Python
├── 📄 README.md                    # Cette documentation
│
├── 🔐 Configuration & Environnement
│   ├── .env                        # Variables d'environnement (LOCAL)
│   ├── .env.sample                 # Modèle d'exemple
│   └── mongo-init.js               # Script initialisation MongoDB
│
├── 📊 Données
│   ├── healthcare_dataset.csv      # Données brutes (à fournir) ← INPUT
│   └── cleaned_healthcare_dataset.csv # Données nettoyées (généré) ← OUTPUT
│
├── 🐍 Scripts Python
│   ├── scripts/
│   │   ├── data_prep.py            # Nettoyage & préparation des données
│   │   └── import_mongo.py         # Import par chunks dans MongoDB
│   │
│   └── tests/
│       ├── test_connection.py      # Tests de connexion & authentification
│       ├── test_database.py        # Tests de schéma & types de données
│       └── test_integrite.py       # Tests d'intégrité des données
│
├── 📚 Documentation
│   ├── pyproject.toml              # Métadonnées du projet Python
│   ├── requirements.txt            # Dépendances Python
│   ├── .gitignore                  # Fichiers ignorés par Git
│   ├── Livrables/                  # Dossier des livrables
│   └── preuves_validation/         # Preuves de validation du projet
│
└── 📦 Fichiers optionnels
    ├── import.ipynb                # Notebook Jupyter (développement)
    ├── main.py                     # Script principal (développement)
    └── create_presentation.py      # Générateur de présentation
```

---

## 🔐 Variables d'environnement

### Fichier `.env` (LOCAL)

Créez un fichier `.env` à la racine du projet avec les variables suivantes :

```bash
# ============================================
# MONGO - AUTHENTIFICATION ADMIN
# ============================================
MONGO_INITDB_ROOT_USERNAME=root
MONGO_INITDB_ROOT_PASSWORD=root
MONGO_INITDB_DATABASE=DataSoluTech

# ============================================
# MONGO - AUTHENTIFICATION APPLICATION
# ============================================
MONGO_APP_USERNAME=user
MONGO_APP_PASSWORD=user

# ============================================
# COLLECTIONS
# ============================================
COLLECTION=Healthcare

# ============================================
# CHEMINS FICHIERS
# ============================================
INPUT_DATA_PATH=/app/data/healthcare_dataset.csv
OUTPUT_DATA_PATH=/app/data/cleaned_healthcare_dataset.csv

# ============================================
# URIS MONGODB
# ============================================
MONGODB_URI=mongodb://user:user@mongodb:27017/DataSoluTech?authSource=DataSoluTech
MONGODB_URI_ROOT=mongodb://root:root@mongodb:27017/admin?authSource=admin
```

### Modèle `.env.sample`

Un fichier `.env.sample` est fourni comme référence. Ne pas modifier ce fichier.

### ⚠️ Notes de sécurité

| Variable | Environnement | Valeur recommandée |
|----------|---------------|-------------------|
| `MONGO_INITDB_ROOT_PASSWORD` | Développement | `root` |
| `MONGO_INITDB_ROOT_PASSWORD` | Production | Mot de passe fort (32+ car.) |
| `MONGO_APP_PASSWORD` | Développement | `user` |
| `MONGO_APP_PASSWORD` | Production | Mot de passe fort (32+ car.) |

⚠️ **IMPORTANT** : Ne jamais commit le fichier `.env` sur Git. Utiliser `.env.sample` comme modèle.

---

## 🚀 Installation et lancement

### Installation initiale

```bash
# 1. Cloner ou télécharger le projet
cd "HealthcareImport-2"

# 2. Créer le fichier .env
cp .env.sample .env
# Puis éditer .env avec vos variables

# 3. Préparer les données
mkdir -p data
cp /chemin/vers/healthcare_dataset.csv ./data/

# 4. Vérifier la structure
ls -la ./data/
ls -la ./scripts/
ls -la ./tests/
```

### Démarrage des services

#### 🟢 Premier démarrage (construction + démarrage)

```bash
# Démarrer en mode interactif (voir les logs en temps réel)
docker compose up --build

# Ou en arrière-plan (détaché)
docker compose up -d --build
```

**Étapes qui se déclenchent** :
1. ✅ Construction de l'image Python
2. ✅ Démarrage de MongoDB (initialisation utilisateurs + schéma)
3. ✅ Démarrage du service Python
4. ✅ Exécution des tests de connexion
5. ✅ Nettoyage des données CSV
6. ✅ Import des données dans MongoDB

#### 🔵 Démarrages suivants (sans reconstruction)

```bash
# Démarrer les services
docker compose up

# Ou en arrière-plan
docker compose up -d

# Redémarrer un service spécifique
docker compose restart python_service
docker compose restart mongodb
```

#### ⛔ Arrêt des services

```bash
# Arrêt gracieux
docker compose stop

# Arrêt et suppression des conteneurs (données persistantes conservées)
docker compose down

# Arrêt, suppression conteneurs ET réinitialisation des données
docker compose down -v
```

### Vérification du démarrage

```bash
# Vérifier l'état des services
docker compose ps

# Voir les logs en temps réel
docker compose logs -f

# Voir les logs d'un service spécifique
docker compose logs -f mongodb
docker compose logs -f python_service

# Attendre le démarrage complet (attendre ~30-60 secondes)
```

---

## 🏗️ Architecture

### Services Docker

#### 🗄️ MongoDB

```yaml
Service: mongodb
Image: mongo:latest
Port: 127.0.0.1:27017:27017
Restart: always
Healthcheck: ✅ Activé (ping toutes les 10s)
```

**Initialisation** :
- Création de 2 utilisateurs (admin + app)
- Création de la collection `Healthcare` avec validation JSON Schema
- Création d'un index unique sur `patient_id`

#### 🐍 Python Service

```yaml
Service: python_service
Build: Dockerfile (Python 3.12+)
Depends on: mongodb (condition: service_healthy)
Healthcheck: ✅ Activé (test endpoint toutes les 30s)
Timeout: 40s avant démarrage du healthcheck
```

**Exécution** :
1. Test de connexion MongoDB
2. Nettoyage des données CSV
3. Import par chunks de 1000 documents

### Volumes

| Type | Nom | Source locale | Destination conteneur | Persistant | Fonction |
|------|-----|----------------|----------------------|-----------|----------|
| Named | `mongodb_data` | Docker volume | `/data/db` | ✅ Oui | Données MongoDB persistantes |
| Bind | - | `./data` | `/app/data` | ✅ Oui | Fichiers CSV input/output |
| Bind | - | `./scripts` | `/app/scripts` | ✅ Oui | Scripts Python |
| Bind | - | `./tests` | `/app/tests` | ✅ Oui | Tests unitaires |
| Bind | - | `./mongo-init.js` | `/docker-entrypoint-initdb.d/` | ✅ Oui | Init MongoDB |

### Réseau Docker

```yaml
Réseau: app_network
Driver: bridge
Scope: Services seulement (mongodb + python_service)
Discovery DNS: Automatique par nom du service
```

**Communication** :
- Python Service → MongoDB : `mongodb://user:user@mongodb:27017/DataSoluTech`
- MongoDB → Python Service : Pas de connexion retour

---

## 📊 Schéma de la base

### Base de données : `DataSoluTech`

### Collection : `Healthcare`

#### Validation JSON Schema

La collection applique un schéma JSON strict au niveau MongoDB :

```javascript
{
   bsonType: "object",
   required: [
      "patient_id",
      "name",
      "age",
      "gender",
      "blood_type",
      "medical_condition",
      "date_of_admission",
      "billing_amount",
      "discharge_date",
      "test_results"
   ],
   properties: { /* voir détails ci-dessous */ }
}
```

#### Schéma détaillé des champs

| Champ | Type | Obligatoire | Contraintes | Exemple |
|-------|------|-------------|-------------|---------|
| `_id` | ObjectId | ✅ Auto | MongoDB auto-généré | ObjectId(...) |
| `patient_id` | Integer | ✅ Oui | Unique, positif | `1`, `2`, `3` |
| `name` | String | ✅ Oui | Max 200 car. | `"Jean Dupont"` |
| `age` | Integer | ✅ Oui | 0-150 | `45` |
| `gender` | String | ✅ Oui | Enum: Male, Female, Other | `"Male"` |
| `blood_type` | String | ✅ Oui | Enum: A+, A-, B+, B-, AB+, AB-, O+, O- | `"O+"` |
| `medical_condition` | String | ✅ Oui | 1-500 car. | `"Obesity"` |
| `date_of_admission` | Date | ✅ Oui | Format ISO 8601 | `ISODate("2026-05-27")` |
| `doctor` | String | ⚠️ Optionnel | Max 200 car. | `"Samantha Davies"` |
| `hospital` | String | ⚠️ Optionnel | Max 200 car. | `"Hôpital Central"` |
| `insurance_provider` | String | ⚠️ Optionnel | Max 100 car. | `"Medicare"` |
| `billing_amount` | Double | ✅ Oui | > 0 | `33643.33` |
| `room_number` | Integer | ⚠️ Optionnel | Positif | `352` |
| `admission_type` | String | ⚠️ Optionnel | Enum: Elective, Urgent, Emergency | `"Emergency"` |
| `discharge_date` | Date | ✅ Oui | Format ISO 8601 | `ISODate("2026-06-10")` |
| `medication` | String | ⚠️ Optionnel | Max 500 car. | `"Ibuprofen"` |
| `test_results` | String | ✅ Oui | Enum: Normal, Abnormal, Inconclusive | `"Inconclusive"` |

#### Document exemple

```javascript
db.Healthcare.findOne()

{
  "_id" : ObjectId("66f1a2c3b4d5e6f7g8h9i0j1"),
  "patient_id" : 1,
  "name" : "Jean Dupont",
  "age" : 45,
  "gender" : "Male",
  "blood_type" : "O+",
  "medical_condition" : "Obesity",
  "date_of_admission" : ISODate("2026-05-27T00:00:00Z"),
  "doctor" : "Samantha Davies",
  "hospital" : "Hôpital Central",
  "insurance_provider" : "Medicare",
  "billing_amount" : 33643.33,
  "room_number" : 352,
  "admission_type" : "Emergency",
  "discharge_date" : ISODate("2026-06-10T00:00:00Z"),
  "medication" : "Ibuprofen",
  "test_results" : "Inconclusive"
}
```

---

## 🔑 Index

### Index unique sur `patient_id`

```javascript
db.Healthcare.createIndex({ patient_id: 1 }, { unique: true })
```

**Propriétés** :
- Type : Unique
- Champs : `patient_id` (ascendant)
- Raison : Éviter les doublons de patients
- Performance : Accélère les recherches par patient_id

**Vérifification** :

```bash
# Lister tous les index
docker compose exec mongodb mongosh -u root -p root --authenticationDatabase admin --eval \
  "use DataSoluTech; db.Healthcare.getIndexes()"
```

**Résultat attendu** :

```javascript
[
  { v: 2, key: { _id: 1 }, name: '_id_' },
  { v: 2, key: { patient_id: 1 }, name: 'patient_id_1', unique: true }
]
```

---

## 👥 Utilisateurs et rôles

### 1️⃣ Utilisateur administrateur

| Propriété | Valeur |
|-----------|--------|
| **Username** | `root` |
| **Password** | `root` |
| **Base d'authentification** | `admin` |
| **Rôles** | `root` (superadmin) |
| **Permissions** | Toutes les opérations sur toutes les bases |

**URI de connexion** :

```
mongodb://root:root@localhost:27017/admin?authSource=admin
```

### 2️⃣ Utilisateur applicatif

| Propriété | Valeur |
|-----------|--------|
| **Username** | `user` |
| **Password** | `user` |
| **Base d'authentification** | `DataSoluTech` |
| **Rôles** | `readWrite` sur `DataSoluTech` |
| **Permissions** | Lecture + Écriture sur `DataSoluTech` |

**URI de connexion** :

```
mongodb://user:user@localhost:27017/DataSoluTech?authSource=DataSoluTech
```

### Création des utilisateurs (automatisée)

Les utilisateurs sont créés automatiquement au premier démarrage par le script `mongo-init.js` :

```javascript
// Utilisateur applicatif
db.createUser({
    user: "user",
    pwd: "user",
    roles: [
        { role: "readWrite", db: "DataSoluTech" }
    ],
    mechanisms: ["SCRAM-SHA-256"]
});
```

### Vérification des utilisateurs

```bash
# Accéder à MongoDB Shell en tant qu'admin
docker compose exec mongodb mongosh -u root -p root --authenticationDatabase admin

# Afficher tous les utilisateurs
db.usersInfo()

# Afficher les permissions d'un utilisateur
db.getUser("user")
```

---

## 🔄 Nettoyage et migration

### Étapes de nettoyage des données

Le script `scripts/data_prep.py` applique les transformations suivantes :

#### 1️⃣ Analyse des valeurs manquantes

```
Valeurs manquantes par colonne:
Doctor                      1512 (4.8%)
Discharge Date              1023 (3.2%)
Insurance Provider            451 (1.4%)
...
```

#### 2️⃣ Suppression des doublons

```
Nombre de lignes en doublon supprimées: 42
```

#### 3️⃣ Génération d'ID unique

```python
data['patient_id'] = data.index
```

Résultat : Chaque ligne reçoit un `patient_id` unique de 0 à N-1.

#### 4️⃣ Renommage des colonnes

Mappage des noms de colonnes CSV vers MongoDB :

| CSV | MongoDB |
|-----|---------|
| `Name` | `name` |
| `Age` | `age` |
| `Gender` | `gender` |
| `Blood Type` | `blood_type` |
| `Medical Condition` | `medical_condition` |
| `Date of Admission` | `date_of_admission` |
| `Doctor` | `doctor` |
| `Hospital` | `hospital` |
| `Insurance Provider` | `insurance_provider` |
| `Billing Amount` | `billing_amount` |
| `Room Number` | `room_number` |
| `Admission Type` | `admission_type` |
| `Discharge Date` | `discharge_date` |
| `Medication` | `medication` |
| `Test Results` | `test_results` |

#### 5️⃣ Normalisation des noms (civilités)

```python
# Avant : "Mr. John Smith", "Dr. Jane Doe"
# Après : "John Smith", "Jane Doe"

data['name'] = data['name'].str.title()
data['name'] = data['name'].str.strip()
data['name'] = data['name'].str.replace(r'\b(Mr\.|Dr\.|Mrs\.|Ms\.)\s*', '', regex=True)
```

#### 6️⃣ Traitement des montants

```python
# Arrondir à 2 décimales
data['billing_amount'] = data['billing_amount'].round(2)

# Décompte des valeurs négatives (alerte)
if data[data['billing_amount'] < 0].shape[0] > 0:
    print(f"ATTENTION: Valeurs négatives : {count}")
```

#### 7️⃣ Normalisation des dates

```python
# Conversion en datetime ISO 8601
data['date_of_admission'] = pd.to_datetime(data['date_of_admission'], errors="coerce")
data['discharge_date'] = pd.to_datetime(data['discharge_date'], errors="coerce")
```

**Résultats** :

| Étape | Input | Output | Variation |
|-------|-------|--------|-----------|
| Format CSV | 31,506 lignes | 31,506 | - |
| Doublons supprimés | 31,506 | 31,464 | -42 (-0.13%) |
| Nettoyage final | 31,464 | 31,464 | ✅ Stable |

### Étapes de migration vers MongoDB

Le script `scripts/import_mongo.py` effectue l'import en chunks :

#### 1️⃣ Lecture du CSV nettoyé

```python
df = pd.read_csv(file_path, parse_dates=['date_of_admission', 'discharge_date'])
```

#### 2️⃣ Connexion à MongoDB

```python
client = pymongo.MongoClient(mongodb_uri)
db = client[db_name]
collection = db[collection_name]
```

#### 3️⃣ Vérification des index

```python
collection.create_index("patient_id", unique=True)
```

#### 4️⃣ Division en chunks

```
Taille du chunk : 1000 documents
Nombre total de chunks : 32 (31,464 / 1000 = 31.464)
Chunk 1 : 1000 documents
Chunk 2 : 1000 documents
...
Chunk 31 : 1000 documents
Chunk 32 : 464 documents
```

#### 5️⃣ Vérification des doublons avant insertion

```python
existing_patients = collection.distinct("patient_id")
new_records = [r for r in chunk if r["patient_id"] not in existing_patients]
```

#### 6️⃣ Import avec gestion des erreurs

```python
try:
    collection.insert_many(new_records, ordered=False)
    print(f"Chunk {i+1}/{num_chunks} importé avec succès")
except BulkWriteError as bwe:
    print(f"Chunk {i+1}/{num_chunks} - Erreurs : {bwe.details}")
```

#### 7️⃣ Rapport final

```
Avant l'import : 0 documents
Après l'import : 31,464 documents
Durée estimée : 30-60 secondes
```

### Procédure de réinitialisation complète

⚠️ **DANGER** : Cela supprime toutes les données !

#### Option 1 : Réinitialisation légère (garder le volume)

```bash
# Arrêter les services
docker compose stop

# Vider la collection
docker compose exec mongodb mongosh -u root -p root --authenticationDatabase admin --eval \
  "use DataSoluTech; db.Healthcare.deleteMany({})"

# Redémarrer
docker compose up
```

#### Option 2 : Réinitialisation complète (tout supprimer)

```bash
# Arrêter et supprimer les conteneurs + volumes
docker compose down -v

# Recommencer
docker compose up --build
```

#### Option 3 : Réinitialisation sélective (garder MongoDB)

```bash
# Arrêter et supprimer le service Python seulement
docker compose down python_service

# Vider la collection
docker compose exec mongodb mongosh -u root -p root --authenticationDatabase admin --eval \
  "use DataSoluTech; db.Healthcare.deleteMany({})"

# Redémarrer le service Python
docker compose up python_service
```

---

## 🧪 Tests réalisés

### 1️⃣ Tests de connexion (`test_connection.py`)

Exécutés **automatiquement** au démarrage du conteneur Python.

#### Test 1.1 : Connexion valide avec identifiants applicatif

```python
def test_connection():
    """Test d'une connexion valide à MongoDB"""
    client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=1000)
    client.admin.command('ping')
    self.assertTrue(True)
```

**Attendu** : ✅ Connexion réussie

#### Test 1.2 : Tentative de connexion avec URI invalide

```python
def test_connection_invalid_uri():
    """Test d'une connexion avec URI invalide"""
    try:
        client = MongoClient(invalid_uri, serverSelectionTimeoutMS=1000)
        client.admin.command('ping')
        self.fail("Connexion avec URI invalide a réussi")
    except errors.ConnectionFailure:
        self.assertTrue(True)
```

**Attendu** : ✅ Connexion rejetée (ConnectionFailure)

#### Test 1.3 : Vérification des identifiants utilisateurs

```python
def test_users_credentials():
    """Vérification que les utilisateurs sont créés"""
    client = MongoClient(mongodb_uri_root)
    db = client[db_name]
    users_info = db.command("usersInfo")
    for user in users_info['users']:
        print(f"Utilisateur: {user['user']}, Rôles: {user['roles']}")
```

**Attendu** : ✅ Affichage de 2 utilisateurs (`root`, `user`)

#### Test 1.4 : Test CRUD complet

```python
def test_database_CRUD():
    """Test de créer, lire, mettre à jour, supprimer"""
    collection.insert_one({"test": "data"})           # CREATE
    found = collection.find_one({"test": "data"})     # READ
    collection.update_one(..., {"$set": {...}})      # UPDATE
    collection.delete_one({"test": "updated_data"})   # DELETE
```

**Attendu** : ✅ Toutes les opérations réussies

### 2️⃣ Tests de schéma (`test_database.py`)

Tests de validation du schéma et intégrité des données.

#### Test 2.1 : Vérification du fichier CSV output

```python
def test_output_csv_existence():
    """Vérifier que le CSV nettoyé existe"""
    self.assertTrue(os.path.exists(output_path))
```

**Attendu** : ✅ Fichier `cleaned_healthcare_dataset.csv` présent

#### Test 2.2 : Vérification des types de données

```python
def test_data_types():
    """Vérifier cohérence entre CSV et MongoDB"""
    csv_schema = get_csv_schema()
    mongo_schema = get_mongo_schema()
    # Comparer types CSV vs MongoDB
```

**Attendu** : ✅ Types cohérents (int, float, string, date)

#### Test 2.3 : Vérification des valeurs nulles

```python
def test_null_values():
    """Comparer les valeurs nulles CSV vs MongoDB"""
    csv_nulls = count_csv_nulls()
    mongo_nulls = count_mongo_nulls()
    self.assertEqual(csv_nulls, mongo_nulls)
```

**Attendu** : ✅ Nombre de nulls identique

### 3️⃣ Tests d'intégrité (`test_integrite.py`)

Tests d'intégrité générale des données.

#### Test 3.1 : Présence des collections

```python
def test_collection_presence():
    """Vérifier que la collection Healthcare existe"""
    db_collections = db.list_collection_names()
    self.assertIn("Healthcare", db_collections)
```

**Attendu** : ✅ Collection `Healthcare` présente

#### Test 3.2 : Comptage des enregistrements

```python
def test_record_count():
    """Vérifier que le nombre de records CSV == records MongoDB"""
    csv_count = len(df_source)
    mongo_count = db["Healthcare"].count_documents({})
    self.assertEqual(csv_count, mongo_count)
```

**Attendu** : ✅ Comptage identique

### Exécution manuelle des tests

```bash
# Exécuter tous les tests
docker compose exec python_service python -m pytest tests/

# Exécuter un test spécifique
docker compose exec python_service python tests/test_connection.py

# Exécuter avec verbose
docker compose exec python_service python -m unittest tests.test_connection -v
```

---
## ⚙️ Commandes utiles

### Gestion des services

```bash
# Démarrer
docker compose up -d --build

# Arrêter
docker compose stop

# Redémarrer
docker compose restart

# Logs en temps réel
docker compose logs -f

# État
docker compose ps
```
### Nettoyage

```bash
# Arrêter sans supprimer les volumes
docker compose down

# Arrêter et supprimer tout (ATTENTION: perte de données)
docker compose down -v

# Supprimer les conteneurs orphelins
docker compose down --remove-orphans

# Nettoyer le système Docker
docker system prune -a
```

---

## 📚 Ressources

### Documentation officielle
- [MongoDB Documentation](https://docs.mongodb.com/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Mongosh Manual](https://docs.mongodb.com/mongosh/current/)

### Outils
- [MongoDB Compass](https://www.mongodb.com/products/compass) - GUI MongoDB
- [Docker Desktop](https://www.docker.com/products/docker-desktop) - Application Docker
- [MongoDB Shell](https://www.mongodb.com/products/shell) - CLI MongoDB

### Fichiers du projet
- `.env` - Variables d'environnement (LOCAL)
- `.env.sample` - Modèle d'exemple
- `docker-compose.yml` - Configuration des services
- `Dockerfile` - Image Python
- `mongo-init.js` - Script d'initialisation MongoDB
- `scripts/data_prep.py` - Nettoyage des données
- `scripts/import_mongo.py` - Import dans MongoDB
- `tests/test_*.py` - Tests unitaires

---

## 👨‍💻 Auteur

**Thomas LECLERCQ**

**Dernière mise à jour** : 16/07/2026

**Statut** : ✅ Production-ready (développement)

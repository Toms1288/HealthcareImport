import json
from hashlib import sha256

# Fichier pour stocker les utilisateurs de manière persistante
USERS_FILE = "users.json"

def hash_password(password):
    """Hache un mot de passe en utilisant SHA-256."""
    return sha256(password.encode('utf-8')).hexdigest()

def load_users():
    """Charge les utilisateurs depuis le fichier JSON."""
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users(users):
    """Sauvegarde les utilisateurs dans le fichier JSON."""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def create_user(username, password, role):
    """Crée un nouvel utilisateur et le sauvegarde."""
    users = load_users()
    if username in users:
        print(f"Erreur: L'utilisateur '{username}' existe déjà.")
        return False

    users[username] = {
        "password": hash_password(password),
        "role": role
    }
    save_users(users)
    return True

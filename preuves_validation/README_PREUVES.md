# Dossier de preuves des corrections suite à la soutenance 



## 1.Lancement complet du projet depuis un environnement vide

Le lancement complet se réalise sans erreur à partir d'un environnement vide.


## 2.Résultat de la commande docker-compose.ps

La commande docker-compose.ps montre le service mongo actif sur l'adresse 127.0.0.1:21017.
Le service python est inactivé une fois que les scripts ont été exécutés.


## 3.Logs montrant que le nettoyage et l'import se termine sans erreur

Le code est présenté dans le fichier data_prep.py pour le nettoyage et import_mongo.py pour l'import dans MongoDB.
Les logs montrent un nettoyage et un import sans erreur.

## 4.Nombres de lignes avant et après nettoyage

Avant le nettoyage, le dataframe compte 55000 lignes.
Suite à la suppression des 534 doublons sont crées 54966 documents.
106 affichent une valeur négatif pour billing_amount, à vérifier avec le métier.

## 5.Nombre de documents présents dans MongoDB

54966 documents sont présents dans MongoDB après l'import.

## 6.Vérification du type BSON Date

Un test de cohérance entre les types de données du CSV et le schéma fourni dans mongo-init.js est réalisé par le script test_integrite. Aucune erreur n'est détectée. Le format BSON Date est correctement appliqué.

## 7.Liste des index MongoDB crées

La colonne patient_id est décalrée dans le fichier mongo-init.js.
La déclaration fonctionne car cette colonne sert de référence lors de l'import des données dans MongoDB. Lorsque les données sont déjà présentes, l'index empeche les doublons. (cf 08_test_sans_doublons)


## 8. Preuve qu'une deuxième exécution ne crée pas de doublons

Lors de l'import, j'ai ajouté une vérification sur les index déjà présents dans la collection. Lors de l'import, les chunks sont donc filtrés et aboutissent à l'import d'aucune nouvelle donnée.

## 9. Refus d'une connexion sans identifiants

Le test de connexion avec un uri invalide abouti à un echec, comme prévu.


## 10.Connexion réussie avec le compte applicatif

Le test de connexion est valide.

## 11. Preuve que le compte applicatif dispose uniquement des droits nécessaires

Le seul compte présent, autre que le root, et le compte user, disposant uniquement des droits 

## 12. Résultats des tests automatisés

Tests réalisés :
test_connection.py
- Connexion avec uri invalide : OK
- Connexion avec compte app : OK
- Roles des comptes créés : OK
- Test CRUD (ajout d'une ligne, lecture, modification et suppression) : OK
test_database.py (sur le csv avant import)
- Présence des colonnes obligatoires indiquées : OK
- Absence de valeurs nulles : OK
- Absence de doublons : OK
- Vérification des Types attendus : OK
- Vérification des formats date : ok
test_integrite.py (collection MongoDB après import)
- Vérification du schéma de données avec le CSV : OK
- Vérification de la cohérance des types de données : OK
- Vérification du nombre de documents MongoDB par rapport aux lignes du CSV : OK

## 13. Arborescence finale du projet

L'arborescence est nettoyée et correspond aux besoins du projet.



## 14. Fichiers Dockerfile, docker-compose, README, présentation mises à jour

Se réferer aux différents fichiers

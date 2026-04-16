# Mission DataSoluTech : Migration 55k Patients

Ce dépôt contient la solution technique pour migrer les 55 500 dossiers patients de DataSoluTech. L'objectif était de passer d'un fichier plat (CSV) à une base NoSQL flexible tout en garantissant l'intégrité des données.

---

## 1. Organisation des fichiers
* **migration.py** : Script principal utilisant pandas et pymongo pour le traitement et l'envoi des données.
* **verify_migration.py** : Script de sécurité pour valider le compte final des documents (55 500 entrées).
* **docker-compose.yml & Dockerfile** : Infrastructure complète (MongoDB + App Python) conteneurisée.
* **requirements.txt** : Dépendances Python nécessaires.

---

## 2. Guide de lancement
Tout est automatisé avec Docker. Pour démarrer l'environnement :

```bash
docker compose up --build -d
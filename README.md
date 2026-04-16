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

3. Détails techniques et Sécurité
Base de données : MongoDB sécurisé avec authentification admin.

Optimisation : Insertion par lots (insert_many) pour la rapidité de traitement.

* **Inspection manuelle** : 
    ```bash
    docker exec -it mongodb mongosh -u admin -p admin
    ```
    (Commandes : use medical_db puis db.patients.countDocuments())

## 4. Évolutions Cloud (AWS)
Le projet est conçu pour être facilement déployé sur Amazon Web Services (AWS) en utilisant les services suivants :

* **Amazon S3** : Pour le stockage sécurisé et durable du fichier source `healthcare_dataset.csv`.
* **Amazon DocumentDB** : Pour remplacer l'instance MongoDB locale par une base de données entièrement gérée et hautement disponible.
* **Amazon ECS (Fargate)** : Pour exécuter le conteneur de migration de manière "Serverless", sans avoir à gérer de serveurs.

---
# Migration NoSQL (MongoDB) — Données médicales DataSoluTech

Ce projet automatise la migration du fichier CSV (55 500 patients) vers **MongoDB** (via `pymongo`) et inclut :
- Validation des données (types, valeurs manquantes, cohérence)
- Insertion par lots (chunks) pour garantir la scalabilité
- Scripts Docker / Compose pour un environnement portable et isolé
- Vérification de l'intégrité des données après migration

---

## 1. Structure du projet

```text
Mission_DataSoluTech/
├── migration.py           # Script principal de migration + CRUD
├── verify_migration.py    # Script de validation du compte (55 500 entrées)
├── requirements.txt       # Dépendances Python (pandas, pymongo)
├── Dockerfile             # Configuration de l'image Python
├── docker-compose.yml     # Orchestration (MongoDB + App Python)
└── healthcare_dataset.csv # Jeu de données source

---

## 2. Prérequis rapides

```text
- Python 3.11+ et Docker / Docker Compose installés sur votre machine
- Avoir lu les ressources NoSQL (MongoDB, scalabilité, sharding, CRUD)
- Dataset CSV : `healthcare_dataset.csv` présent à la racine du projet

---

## 3. Configuration

| Fichier | Rôle |
| :--- | :--- |
| `.env` | Contient les variables d'environnement (connexion, noms des collections) |
| `docker-compose.yml` | Définit les services (MongoDB, Mongo Express, App) |
| `migration.py` | Script principal de migration des données du CSV vers MongoDB |
| `healthcare_dataset.csv` | Jeu de données médicales à importer |
| `validate.py` | Vérifie et nettoie les données avant la migration |

---

## 4. Lancer avec Docker

```text

```bashs
docker compose up --build

L'application `app` lancera la migration automatiquement.  
Le dashboard **mongo-express** est accessible sur : [http://localhost:8081](http://localhost:8081)

---

## 5. Variables Docker


| Variable | Description |
| :--- | :--- |
| `MONGO_INITDB_ROOT_USERNAME` | Nom d'utilisateur administrateur MongoDB |
| `MONGO_INITDB_ROOT_PASSWORD` | Mot de passe administrateur MongoDB |
| `MONGODB_URI` | Chaîne de connexion utilisée par le script `migration.py` |
| `ME_CONFIG_MONGODB_AUTH_DATABASE` | Base ciblée par Mongo Express (`medical_db`) |

---

## 6. Tests et qualité

```text

Lancer les tests unitaires : 
```bash
pytest tests/

### 6.1 Vérification manuelle (Shell)

```text

Pour vérifier les données directement dans la base, connectez-vous au shell MongoDB :
```bash
docker exec -it mongodb mongosh -u admin -p admin


## 7. Opérations CRUD

```text

Le projet implémente les opérations fondamentales pour la gestion des dossiers patients, permettant une manipulation flexible des données :

* **Create** : Insertion automatisée des 55 500 enregistrements via le script `migration.py`.
* **Read** : Consultation des dossiers via le shell MongoDB ou l'interface Mongo Express.
* **Update** : Mise à jour possible des diagnostics, traitements ou informations de sortie.
* **Delete** : Suppression sécurisée de documents si nécessaire.

---

## 8. Ajout d'un nouvel utilisateur MongoDB

```text

Pour sécuriser l'accès et permettre une évaluation externe, vous pouvez créer un utilisateur avec des droits spécifiques sur la base de données :

```javascript
db.createUser({
  user: "Evaluateur",
  pwd: "Evaluateurpass",
  roles: [{ role: "readWrite", db: "medical_db" }]
})
Commande de connexion pour l'utilisateur créé :
docker exec -it mongodb mongosh -u Evaluateur -p Evaluateurpass --authenticationDatabase medical_db

---

## 10. Déploiement AWS (Perspectives)

```text

Le projet est conçu pour être facilement porté sur l'infrastructure **Amazon Web Services (AWS)** afin de garantir une haute disponibilité et une scalabilité accrue :

* **Amazon S3** : Utilisé pour le stockage sécurisé et durable des fichiers sources CSV et des sauvegardes (backups).
* **Amazon DocumentDB** : Pour remplacer l'instance locale par une base de données NoSQL entièrement gérée, hautement disponible et compatible avec l'API MongoDB.
* **Amazon ECS / Fargate** : Pour exécuter le script de migration en mode conteneurisé "Serverless", sans avoir à gérer de serveurs physiques.
* **AWS IAM** : Pour une gestion fine des accès et de la sécurité des données médicales.

---

## 11. Licence

```text

Projet 5 Cherif Dorra réalisé dans le cadre de la **Mission DataSoluTech** — Migration NoSQL sécurisée.  
© 2026 — Tous droits réservés.


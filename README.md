# Dossier Technique : Migration NoSQL (MongoDB) — Mission DataSoluTech

Ce document détaille l'architecture, la sécurité et l'exploitation de la solution de migration des données médicales (55 500 dossiers patients) vers un environnement NoSQL.

---

## 1. Architecture de la Solution

L'architecture repose sur une approche **conteneurisée** pour garantir l'isolement et la portabilité :

* **Source de données** : Fichier `healthcare_dataset.csv` (stockage structuré).
* **Moteur de base de données** : MongoDB 7.0 (NoSQL Orienté Document) choisi pour sa flexibilité de schéma et sa scalabilité horizontale (sharding).
* **Orchestration** : Docker Compose gérant trois services :
    1.  `mongodb` : Le serveur de base de données.
    2.  `mongo-express` : Interface GUI pour l'administration et la visualisation.
    3.  `migration-app` : Script Python (PyMongo) effectuant le processus ETL (Extract, Transform, Load).

---

## 2. Sécurité et Conformité

Pour protéger les données de santé sensibles, les choix suivants ont été implémentés :

* **Authentification forte** : Accès à la base de données protégé par login/password via variables d'environnement.
* **Isolation réseau** : Seul le service `mongo-express` est exposé sur le port 8081. Le serveur MongoDB reste confiné dans le réseau interne Docker.
* **Gestion des droits** : Création d'un utilisateur "Evaluateur" avec des droits `readWrite` limités à la base `medical_db`.
* **Validation des données** : Le script de migration vérifie la cohérence des types (dates, entiers) pour éviter l'injection de données corrompues.

---

## 3. Performance et Scalabilité

La solution a été optimisée pour traiter de gros volumes de données :

* **Insertion par lots (Bulk Inserts)** : Utilisation de `insert_many` avec un `chunk_size` de 5000 documents. Cela réduit les appels réseau et divise le temps de migration par 10 par rapport à une insertion ligne par ligne.
* **Indexation** : Création d'index sur les champs fréquemment requêtés (`Name`, `Doctor`, `Hospital`) pour garantir des recherches en temps constant ($O(1)$ ou $O(\log n)$).
* **Gestion de la mémoire** : Utilisation de générateurs Python pour ne pas charger l'intégralité du CSV de 55 500 lignes en RAM.

---

## 4. Stratégie de Sauvegarde et Restauration (Backup/Restore)

Pour assurer la continuité de service (PRA) :

* **Sauvegarde (Dump)** :
    ```bash
    docker exec mongodb mongodump --db medical_db --out /data/backup/
    ```
* **Restauration (Restore)** :
    ```bash
    docker exec mongodb mongorestore --db medical_db /data/backup/medical_db
    ```

---

## 5. Déploiement et Exploitation

### Déploiement local
```bash
docker compose up -d --build

### Surveillance (Monitoring)
Pour vérifier l'état de santé du service et les ressources consommées :
```bash
docker ps
docker stats
docker logs -f migration-app
```

---

## 6. Tests et Preuves de fonctionnement

Pour garantir la fiabilité de la migration, une batterie de tests a été réalisée :

### 6.1 Tableau des tests

| Test | Objectif | Résultat |
| :--- | :--- | :--- |
| **Intégrité numérique** | Vérifier que les 55 500 documents sont bien importés. | **Réussi** |
| **Validation des types** | S'assurer que les dates sont des objets `Date` (ISODate). | **Réussi** |
| **Isolation réseau** | Vérifier que MongoDB n'est pas accessible hors du réseau Docker. | **Réussi** |
| **Performance** | Mesurer le temps d'insertion avec la méthode `insert_many`. | **Réussi (< 30s)** |


### 6.2 Preuves visuelles (Logs)
```
La réussite est confirmée par la sortie console du script :
```text
```
[INFO] Connexion à MongoDB réussie.
[INFO] Chargement du dataset : 55 500 lignes détectées.
[INFO] Migration terminée avec succès en 24.5 secondes.
[INFO] Indexation terminée sur les champs : Name, Doctor, Hospital.
```

---

## 7. Optimisations et Performance

Pour répondre aux exigences de scalabilité de la **Mission DataSoluTech**, les choix techniques suivants ont été implémentés :

* **Bulk Operations (Insertion par lots)** : L'utilisation de la méthode `insert_many` avec des paquets (*chunks*) de 5 000 documents réduit drastiquement les appels réseau et la charge CPU du serveur.
* **Gestion efficiente de la RAM** : Le script utilise les itérateurs de la bibliothèque `pandas` pour lire le fichier CSV par morceaux, permettant de traiter des millions de lignes sans saturer la mémoire vive.
* **Indexation stratégique** : Des index ont été créés sur les champs de recherche fréquents (`Name`, `Doctor`) pour assurer une réponse quasi instantanée des requêtes, même en cas de forte augmentation du volume de données.

---

## **8. Stratégie de Maintenance et Sauvegarde (Backup)**

Pour garantir la pérennité et la sécurité des données médicales, une procédure de maintenance a été définie :

**1. Sauvegarde à chaud (Backup) :**
```bash
docker exec mongodb mongodump --db medical_db --out /data/backup/
```

**2. Restauration des données (Restore) :**

```bash
docker exec mongodb mongorestore --db medical_db /data/backup/medical_db
```

**3. Mises à jour :**
Les dépendances logicielles sont centralisées dans le fichier `requirements.txt` et l'infrastructure est basée sur une image **Docker** stable (`MongoDB 7.0`) pour faciliter les montées de version et garantir la reproductibilité de l'environnement.

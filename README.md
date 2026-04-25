# Dossier Technique : Migration NoSQL (MongoDB) — Mission DataSoluTech

Ce document détaille l'architecture, la sécurité et l'exploitation de la solution de migration des données médicales (55 500 dossiers patients) vers un environnement NoSQL.

---

## 1. Architecture de la Solution
L'architecture repose sur une approche **conteneurisée** (Docker) pour garantir l'isolement et la portabilité :
* **Source** : Fichier `healthcare_dataset.csv`.
* **Base de données** : MongoDB 7.0 (NoSQL Orienté Document).
* **Application** : Script Python 3.11 utilisant PyMongo et Pandas.

---

## 2. Sécurité et Conformité (Priorité 1)
Conformément aux exigences de sécurité pour les données de santé :
* **Identifiants sécurisés** : Toute référence aux identifiants par défaut (`admin:admin`) a été supprimée du code source.
* **Variables d'Environnement** : L'URI de connexion est injectée via la variable `MONGODB_URI`. 
* **Arrêt Critique** : Le script est configuré pour s'arrêter immédiatement avec un message d'erreur explicite si les secrets de connexion sont manquants, empêchant toute faille de sécurité en production.

---

## 3. Qualité et Nettoyage des Données (Priorité 5)
Le script de migration n'est pas un simple transfert ; il effectue un nettoyage automatique :
* **Suppression des doublons** : Identification et suppression des entrées dupliquées (basé sur le nom et l'âge).
* **Sélection de colonnes** : Seules les données médicales pertinentes sont migrées (`Name`, `Age`, `Gender`, `Blood Type`, `Medical Condition`).
* **Normalisation** : Nettoyage des espaces blancs dans les noms pour garantir l'intégrité des recherches.

---

## 4. Dépendances et Docker (Priorités 2 & 3)
* **Versions Figées** : Les bibliothèques (`pandas`, `pymongo`, `python-dotenv`) sont verrouillées dans le fichier `requirements.txt` pour éviter toute rupture de compatibilité.
* **Dockerfile Optimisé** : L'image Docker utilise désormais le fichier de dépendances pour une installation automatisée et reproductible.

---

## 5. Déploiement et Exploitation

### Configuration
Créez un fichier `.env` à la racine :
```text
MONGODB_URI=mongodb://votre_user:votre_password@mongodb:27017/
```

### Lancement
```bash
docker compose up -d --build
```

### Vérification
```bash
# Vérifier les logs du nettoyage et de la migration
docker logs -f migration-app
# Lancer le script de vérification d'intégrité
python verify_migration.py
```

---

## 6. Tests et Preuves de fonctionnement
| Test | Objectif | Résultat |
| :--- | :--- | :--- |
| **Sécurité Fallback** | Vérifier l'arrêt du script sans variable d'env. | **Réussi (Error Code 1)** |
| **Doublons** | S'assurer de l'unicité des patients. | **Réussi** |
| **Intégrité** | Comparer le nombre d'entrées CSV vs MongoDB. | **Réussi** |
| **Performance** | Temps d'insertion via Bulk Insert. | **Réussi (< 30s)** |

---
*Développé pour la Mission DataSoluTech - Avril 2026*

---

## 4. Structure des Documents (Schéma MongoDB)
Suite au nettoyage des données (Priorité 5), chaque document dans la collection `patients` suit ce modèle JSON :

```json
{
  "_id": "ObjectId",
  "Name": "String (Nettoyé)",
  "Age": "Integer",
  "Gender": "String",
  "Blood Type": "String",
  "Medical Condition": "String"
}
```

**Note** : Les doublons basés sur le couple (Name, Age) sont éliminés lors de la migration.

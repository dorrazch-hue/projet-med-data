# 🏥 Mission DataSoluTech : Migration NoSQL

Ce projet assure la migration sécurisée et optimisée de 55 500 dossiers patients vers MongoDB.

---

## 1. Installation et Lancement
### Pré-requis
* Docker & Docker Compose
* Un fichier `.env` à la racine contenant :
  ```text
  MONGODB_URI=mongodb://utilisateur:password@mongodb:27017/healthcare_db
  ```

### Commandes
```bash
docker compose up -d --build
```

---

## 2. Architecture & Environnement
* **Stack Technique** : Python 3.11-slim, MongoDB 7.0.
* **Gestion des dépendances** : Les versions sont strictement définies dans `requirements.txt` pour garantir la stabilité de l'environnement.
* **Conteneurisation** : Le Dockerfile est optimisé pour une installation automatisée et reproductible des bibliothèques nécessaires.

---

## 3. Sécurité et Confidentialité
* **Gestion des secrets** : Aucune donnée d'authentification n'est stockée en dur dans le code.
* **Validation de connexion** : Le script intègre une vérification de la variable `MONGODB_URI` et s'interrompt en cas de configuration manquante.
* **Isolation** : La base de données MongoDB est isolée au sein du réseau interne Docker.

---

## 4. Traitement des Données et Schéma
### Nettoyage des données
* Suppression des doublons (basée sur l'unicité Nom/Âge).
* Sélection exclusive des colonnes médicales pertinentes.
* Normalisation des chaînes de caractères.

### Structure des Documents (JSON)
Chaque patient est stocké selon le modèle suivant :
```json
{
  "_id": "ObjectId",
  "Name": "String",
  "Age": "Integer",
  "Gender": "String",
  "Blood Type": "String",
  "Medical Condition": "String"
}
```

---

## 5. Validation du Processus
| Test | Objectif | État |
| :--- | :--- | :--- |
| **Sécurité** | Blocage si configuration absente | ✅ Réussi |
| **Intégrité** | Correspondance des volumes CSV/MongoDB | ✅ Réussi |
| **Qualité** | Absence de doublons en base | ✅ Réussi |

---
*Dossier Technique - Dorra - 2026*

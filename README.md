# Mission DataSoluTech : Pipeline de Migration NoSQL Sécurisé

Ce projet présente une solution technique pour la migration, le nettoyage et la sécurisation de 55 500 dossiers médicaux vers une infrastructure MongoDB conteneurisée.

---

## 1. Architecture et Stack Technique

L'application est entièrement conteneurisée pour garantir la portabilité et la reproductibilité du pipeline.

- **Moteur de traitement** : Python 3.11-slim
- **Base de données** : MongoDB 7.0 avec indexation optimisée
- **Scalabilité** : Traitement par flux (chunks de 5 000 lignes) pour minimiser l'usage RAM
- **Environnement** : Docker Compose avec réseau isolé `app-network`

---

## 2. Sécurité et Contrôle d'Accès

### Gestion des Secrets
- Aucune information sensible n'est codée en dur — fichier `.env` exclusivement
- Le script s'arrête si `MONGODB_URI` est absente
- Le fichier `.env` est dans `.gitignore` — jamais commité

### Matrice des Rôles RBAC

| Rôle | Utilisateur | Droits | Usage |
| :--- | :--- | :--- | :--- |
| **Root** | root | root (via Docker) | Démarrage initial du conteneur |
| **Admin** | dbadmin | dbAdminAnyDatabase | Maintenance, index, compactage |
| **App** | migrator | readWrite sur `medical_db` | Insertion et nettoyage des données |
| **Audit** | auditor | read sur `medical_db` | Lecture seule pour évaluation |

### Preuves de Sécurité
Le script `proof_security.py` démontre :
1. La liste complète des utilisateurs (`db.getUsers()`)
2. Que l'utilisateur `auditor` ne peut pas écrire
3. Qu'un accès sans authentification est refusé

---

## 3. Schéma de la Collection `patients`

```json
{
  "personal_info": {
    "name": "String — strip() appliqué",
    "age": "Integer — conversion forcée",
    "gender": "String",
    "blood_type": "String"
  },
  "medical_info": {
    "condition": "String — Unknown si null",
    "medication": "String — Unknown si null",
    "test_results": "String — Unknown si null"
  },
  "admission_info": {
    "admission_date": "Date (datetime UTC)",
    "discharge_date": "Date (datetime UTC)",
    "admission_type": "String",
    "room_number": "Integer",
    "doctor": "String",
    "hospital": "String",
    "duration_days": "Integer — calculé"
  },
  "administrative_info": {
    "insurance_provider": "String",
    "billing_amount": "Float — négatifs remplacés par 0.0"
  },
  "metadata": {
    "source_file": "String",
    "migrated_at": "Date UTC",
    "is_duplicate_removed": "Boolean"
  }
}
```

### Règle de Dédoublonnage
Clé retenue : **Name + Age + Doctor + Hospital + Date of Admission**

Ce choix est plus robuste que Name + Age seul — deux patients homonymes de même âge peuvent avoir des hospitalisations différentes.

---

## 4. Index Créés

| Nom | Champ | Justification |
| :--- | :--- | :--- |
| `_id_` | `_id` | Index par défaut MongoDB |
| `idx_name` | `personal_info.name` | Recherche par patient |
| `idx_condition` | `medical_info.condition` | Filtrage par pathologie |
| `idx_hospital` | `admission_info.hospital` | Requêtes par établissement |
| `idx_doctor` | `admission_info.doctor` | Requêtes par médecin |
| `idx_admission_date` | `admission_info.admission_date` | Filtrage temporel |
| `idx_hospital_date` | `hospital` + `admission_date` (composé) | Recherches combinées fréquentes |

---

## 5. Qualité des Données

| Transformation | Détail |
| :--- | :--- |
| Strip des chaînes | `.str.strip()` sur tous les champs texte |
| Valeurs nulles | Remplacées par `Unknown` ou `0` |
| Conversion Age | `pd.to_numeric` → `int`, 0 si NaN |
| Conversion dates | `pd.to_datetime` → ligne rejetée si invalide |
| Billing négatif | Remplacé par `0.0` |

---

## 6. Rapport de Migration

```
Lignes lues depuis le CSV      : 55 500
Doublons détectés et supprimés : 534
Lignes invalides rejetées      : 0
Documents migrés en base       : 54 966
```

---

## 7. Tests

```bash
# Tests unitaires
python3 -m pytest test_migration.py -v -m "not integration"

# Tests d'intégration (MongoDB requis)
python3 -m pytest test_migration.py -v -m integration
```

---

## 8. Déploiement AWS

- **Amazon DocumentDB** : Cluster NoSQL géré, compatible MongoDB
- **AWS Fargate** : Exécution Serverless du script de migration
- **Amazon S3** : Stockage CSV avec archivage Glacier après 30 jours
- **AWS KMS** : Chiffrement AES-256 au repos, TLS 1.2 en transit
- **AWS CloudWatch** : Surveillance CPU/RAM et logs
- **Estimation** : ~15 USD/mois pour une instance `t4g.medium`

---

## 9. Guide de Lancement

```bash
# 1. Configurer les secrets
cp .env.example .env

# 2. Démarrer les conteneurs
docker compose up -d --build

# 3. Vérifier l'intégrité
python3 verify_migration.py

# 4. Preuves de sécurité
docker exec migration-app python3 proof_security.py

# 5. Lancer les tests
python3 -m pytest test_migration.py -v
```

---
*Dossier Technique — Dorra — 2026*
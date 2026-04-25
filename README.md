# Mission DataSoluTech : Pipeline de Migration NoSQL Sécurisé

Ce projet présente une solution technique pour la migration, le nettoyage et la sécurisation de 55 500 dossiers médicaux vers une infrastructure MongoDB.

---

## 1. Architecture et Stack Technique
L'application est conteneurisée pour garantir la portabilité et la reproductibilité du pipeline.
* **Moteur de traitement** : Python 3.11-slim.
* **Base de données** : MongoDB 7.0 avec indexation optimisée.
* **Scalabilité** : Traitement par flux (Chunks de 5000 lignes) via générateurs Python pour minimiser l'utilisation de la mémoire RAM.
* **Environnement** : Docker Compose avec isolation réseau.

---

## 2. Sécurité et Contrôle d'Accès
### Gestion des Secrets
* **Variables d'environnement** : Aucune information sensible (URI, mots de passe) n'est codée en dur. Le système utilise exclusivement un fichier .env.
* **Protection** : Le script interrompt son exécution si la configuration de sécurité est absente ou incomplète.

### Matrice des Rôles RBAC
| Rôle | Utilisateur | Droits | Usage |
| :--- | :--- | :--- | :--- |
| **Admin** | root | root | Maintenance du serveur |
| **App** | migrator | readWrite | Insertion et nettoyage des données |
| **Audit** | auditor | read | Lecture seule pour évaluation |

---

## 3. Stratégie de Données et Qualité
### Schéma de la Collection patients
| Champ | Type Source | Type MongoDB | Transformation appliquée | Index |
| :--- | :--- | :--- | :--- | :--- |
| **Name** | String | String | Suppression des espaces (Stripping) | Oui |
| **Age** | String/Mix | Integer | Conversion numérique forcée | Non |
| **Medical Condition**| String | String | Valeur par défaut Unknown | Oui |
| **Blood Type** | String | String | Normalisation des caractères | Non |

### Nettoyage et Intégrité
1. **Dédoublonnage** : Suppression des entrées redondantes basées sur le couple Nom et Âge.
2. **Gestion des Manquants** : Remplacement des valeurs nulles pour garantir la continuité du schéma.
3. **Validation** : Utilisation du script verify_migration.py pour contrôler la conformité des types après insertion.

---

## 4. Validation et Tests
### Tests Automatisés
La logique de nettoyage est validée via une suite de tests Pytest :
```bash
python3 -m pytest test_migration.py
```

### Rapport d'intégrité final
```text
--- RAPPORT D'INTÉGRITÉ POST-MIGRATION ---
Documents en base : 54966
Index détectés : _id_, Name_1, Medical_Condition_1
Validation des types : Age (Integer), Name (String)
```
*Le détail complet est consigné dans le fichier logs_final.txt.*

---

## 5. Déploiement et Gouvernance Cloud AWS
La solution est conçue pour une migration vers l'écosystème Amazon Web Services (AWS) répondant aux standards de sécurité des données de santé.

### Infrastructure Cible
* **Amazon DocumentDB** : Cluster de base de données NoSQL géré, hautement disponible et compatible MongoDB.
* **AWS Fargate** : Exécution du script de migration en mode Serverless (Container-as-a-Service), éliminant la gestion de serveurs EC2.
* **Amazon S3** : Stockage sécurisé des fichiers CSV sources avec cycle de vie (archivage automatique vers Glacier après 30 jours).

### Monitoring et Performance
* **AWS CloudWatch** : Surveillance en temps réel des métriques CPU/RAM et agrégation des logs d'erreurs pour alertage immédiat.
* **AWS X-Ray** : Analyse des temps de réponse lors de l'insertion des batchs de données.

### Sécurité et Sauvegarde
* **AWS Backup** : Politique de sauvegarde automatisée avec rétention de 30 jours.
* **Chiffrement** : Utilisation de **AWS KMS** (Key Management Service) pour le chiffrement des données au repos (AES-256) et TLS 1.2 en transit.
* **VPC Isolation** : Déploiement de la base de données dans un sous-réseau privé sans accès direct depuis Internet.

### Analyse des Coûts (FinOps)
* **Estimation mensuelle** : Environ 15 USD pour une instance de type *t4g.medium*.
* **Optimisation** : Utilisation d'instances Spot pour le traitement batch et mise en place d'alertes de budget AWS pour éviter les dépassements.

---

## 6. Guide de lancement
1. **Configuration** : Initialiser le fichier .env.
2. **Déploiement** : `docker compose up -d --build`
3. **Vérification** : `python3 verify_migration.py`

---
Dossier Technique - Dorra - 2026

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
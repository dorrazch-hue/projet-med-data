# Mission DataSoluTech : Pipeline de Migration NoSQL

Ce projet présente une solution industrielle pour la migration, le nettoyage et la sécurisation de 55 500 dossiers médicaux vers une infrastructure NoSQL.

---

## Architecture et Stack
L'application est entièrement conteneurisée pour garantir une portabilité totale.
* **Moteur de traitement** : Python 3.11-slim (optimisé pour le poids de l'image).
* **Base de données** : MongoDB 7.0 avec indexation de performance.
* **Gestion des flux** : Traitement par batchs (Chunks) pour minimiser l'empreinte RAM.

---

## Securite et Robustesse
* **Zero Secrets** : Utilisation exclusive de variables d'environnement (.env).
* **Fail-Fast** : Le système s'interrompt immédiatement si la configuration est corrompue.
* **Tests Automatises** : Validation de la logique de nettoyage via Pytest.

---

## Strategie de Donnees (Data Quality)
### Modele Document (JSON)
```json
{
  "_id": "ObjectId",
  "Name": "String (Sanitized)",
  "Age": "Integer",
  "Gender": "String",
  "Blood Type": "String",
  "Medical Condition": "String"
}
```
### Nettoyage Intelligent
1. **Dedoublonnage** : Suppression des entrees redondantes sur le couple Nom/Age.
2. **Casting** : Conversion forcee des types (ex: ages invalides convertis en 0).
3. **Normalisation** : Suppression des espaces inutiles (Stripping).

---

## Deploiement et Cloud (AWS)
Le projet est conçu pour être deploye sur Amazon Web Services :
* **Base de donnees** : Amazon DocumentDB.
* **Supervision** : AWS CloudWatch pour le monitoring des performances.
* **Continuite** : AWS Backup pour une retention de 30 jours.
* **FinOps** : Budget maîtrise (<15$/mois) avec alertes de seuil.

---

## Lancement Rapide
1. **Configuration** : Creer un fichier .env (voir .env.example).
2. **Build et Start** :
    ```bash
    docker compose up -d --build
    ```
3. **Verification** :
    ```bash
    python3 -m pytest test_migration.py
    ```

---
*Dossier Technique - Dorra - 2026*

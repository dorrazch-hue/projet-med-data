Rapport de Migration : Dataset Médical vers MongoDB
Ce dépôt contient la solution technique pour migrer les 55 500 dossiers patients de DataSoluTech. L'objectif était de passer d'un fichier plat (CSV) à une base NoSQL flexible tout en garantissant qu'aucune donnée ne soit perdue en route.

1. Organisation des fichiers
migration.py : Mon script Python. Il utilise pandas pour traiter le CSV et pymongo pour l'envoi vers la base.

verify_migration.py : Un script de sécurité. Je l'ai créé pour compter les entrées après l'import et confirmer qu'on a bien les 55 500 documents en base.

docker-compose.yml & Dockerfile : Pour monter l'infrastructure (MongoDB + l'app) sans rien installer sur la machine hôte.

requirements.txt : Les librairies nécessaires (pymongo et pandas).

2. Guide de lancement
Tout est automatisé avec Docker. Pour démarrer la base et préparer l'environnement :

Bash
docker compose up --build -d
Exécuter les scripts
Une fois les conteneurs lancés, on lance la migration manuellement :

Bash
docker compose run app python migration.py
Et pour vérifier que tout est bien arrivé :

Bash
docker compose run app python verify_migration.py
3. Détails techniques et Sécurité
Base de données : MongoDB sécurisé avec un utilisateur admin.

Méthode d'import : J'ai choisi l'insertion par lots (insert_many) pour que la migration soit rapide malgré le volume de données.

Vérification manuelle :
On peut entrer dans le conteneur pour inspecter les données :

Bash
docker exec -it mongodb mongosh -u admin -p admin
Commandes utiles :

use medical_db

db.patients.countDocuments()

4. Évolutions vers le Cloud (AWS)
Pour passer en production, j'ai prévu une structure compatible avec les services managés d'Amazon :

Le fichier CSV peut être stocké sur Amazon S3.

La base MongoDB peut être remplacée par Amazon DocumentDB sans changer le code de migration.

Le script peut tourner sur un cluster ECS (Fargate) pour gérer de plus gros volumes de données.


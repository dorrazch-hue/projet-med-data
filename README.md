#  Mission Migration DataSoluTech - MongoDB & Docker

##  Contexte
Ce projet automatise la migration d'un dataset médical (55 500 patients) vers une base de données MongoDB sécurisée et conteneurisée.

##  Comment lancer le projet
1. **Lancer les services :**
   `docker compose up -d --build`
2. **Exécuter la migration :**
   `docker compose run app python migration.py`

##  Sécurité & Authentification
Le système utilise un utilisateur **root** défini via les variables d'environnement dans le fichier docker-compose.
- **Login :** admin
- **Mot de passe :** admin

##  Point Technique : Conteneurs vs Machines Virtuelles (VM)
Point important de la mission :
- **Machine Virtuelle :** Emporte un système d'exploitation complet (lourd et lent).
- **Conteneur Docker :** Partage le "moteur" (le noyau) de l'ordinateur hôte. C'est beaucoup plus léger et rapide, ce qui permet la **scalabilité** demandée par le client.

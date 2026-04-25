FROM python:3.11-slim

# Définir le dossier de travail
WORKDIR /app

# 1. Copier d'abord le fichier de dépendances (Optimisation Docker)
COPY requirements.txt .

# 2. Installer les dépendances figées (Priorité 3)
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copier le reste des fichiers
COPY . .

# Lancer la migration
CMD ["python", "migration.py"]

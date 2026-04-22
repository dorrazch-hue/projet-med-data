// On bascule sur la base de données médicale
db = db.getSiblingDB('medical_db');

// On crée l'utilisateur "employé" avec des droits limités
db.createUser({
  user: "medical_app",
  pwd: "medical_app_password",
  roles: [
    { role: "readWrite", db: "medical_db" }
  ]
});
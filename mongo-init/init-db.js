// On récupère les informations "en direct" depuis Docker
var dbName = process.env.DATABASE_NAME;
var appUser = process.env.MONGO_APP_USER;
var appPass = process.env.MONGO_APP_PASSWORD;

// On se connecte à la base de données
db = db.getSiblingDB(dbName);

// On crée l'utilisateur avec les infos reçues
db.createUser({
  user: appUser,
  pwd: appPass,
  roles: [{ role: "readWrite", db: dbName }],
});
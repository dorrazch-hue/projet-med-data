var dbName    = process.env.DATABASE_NAME;
var appUser   = process.env.MONGO_APP_USER;
var appPass   = process.env.MONGO_APP_PASSWORD;
var auditUser = process.env.MONGO_AUDIT_USER;
var auditPass = process.env.MONGO_AUDIT_PASSWORD;

db = db.getSiblingDB(dbName);

// 1. migrator (readWrite)
db.createUser({
  user: appUser,
  pwd:  appPass,
  roles: [{ role: "readWrite", db: dbName }],
});
print("Utilisateur cree : " + appUser + " (readWrite)");

// 2. auditor (read only)
db.createUser({
  user: auditUser,
  pwd:  auditPass,
  roles: [{ role: "read", db: dbName }],
});
print("Utilisateur cree : " + auditUser + " (read only)");

// 3. dbadmin (admin) - mot de passe fixe car MONGO_ROOT_PASSWORD
// n'est pas accessible dans le contexte d'initialisation MongoDB
db = db.getSiblingDB("admin");
db.createUser({
  user: "dbadmin",
  pwd:  "dbadminPassword123",
  roles: [
    { role: "dbAdminAnyDatabase", db: "admin" },
    { role: "readWriteAnyDatabase", db: "admin" },
  ],
});
print("Utilisateur cree : dbadmin (dbAdminAnyDatabase)");
var dbName    = process.env.DATABASE_NAME;
var appUser   = process.env.MONGO_APP_USER;
var appPass   = process.env.MONGO_APP_PASSWORD;
var auditUser = process.env.MONGO_AUDIT_USER;
var auditPass = process.env.MONGO_AUDIT_PASSWORD;

db = db.getSiblingDB(dbName);

db.createUser({
  user: appUser,
  pwd:  appPass,
  roles: [{ role: "readWrite", db: dbName }],
});
print("Utilisateur cree : " + appUser + " (readWrite)");

db.createUser({
  user: auditUser,
  pwd:  auditPass,
  roles: [{ role: "read", db: dbName }],
});
print("Utilisateur cree : " + auditUser + " (read only)");
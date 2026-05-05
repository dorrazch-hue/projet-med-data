// ============================================================
//  init-db.js  —  Initialisation des utilisateurs MongoDB
//  Exécuté automatiquement au premier démarrage du conteneur
// ============================================================

var dbName    = process.env.DATABASE_NAME;
var appUser   = process.env.MONGO_APP_USER;
var appPass   = process.env.MONGO_APP_PASSWORD;
var auditUser = process.env.MONGO_AUDIT_USER;
var auditPass = process.env.MONGO_AUDIT_PASSWORD;

// Se connecter à la base applicative
db = db.getSiblingDB(dbName);

// ── 1. Utilisateur migrator (readWrite) ─────────────────────
db.createUser({
  user: appUser,
  pwd:  appPass,
  roles: [{ role: "readWrite", db: dbName }],
});
print("✅ Utilisateur créé : " + appUser + " (readWrite)");

// ── 2. Utilisateur auditor (read) ───────────────────────────
db.createUser({
  user: auditUser,
  pwd:  auditPass,
  roles: [{ role: "read", db: dbName }],
});
print("✅ Utilisateur créé : " + auditUser + " (read only)");

// ── 3. Utilisateur dbadmin (admin) ───────────────────────────
db = db.getSiblingDB("admin");
db.createUser({
  user: "dbadmin",
  pwd:  process.env.MONGO_ROOT_PASSWORD,
  roles: [
    { role: "dbAdminAnyDatabase", db: "admin" },
    { role: "readWriteAnyDatabase", db: "admin" },
  ],
});
print("✅ Utilisateur créé : dbadmin (dbAdminAnyDatabase)");
const { Pool } = require('pg');

const pool = new Pool({
  user: 'votre_utilisateur',
  host: 'localhost',
  database: 'votre_base_de_donnees',
  password: 'votre_mot_de_passe',
  port: 5432, // Port par défaut pour PostgreSQL
});

module.exports = pool;

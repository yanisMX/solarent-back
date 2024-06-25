const Sequelize = require('sequelize');
const sequelize = require('../sequelize');

const City = sequelize.define('city', {
  code_name: {
    type: Sequelize.STRING,
    primaryKey: true
  },
  name: Sequelize.STRING,
  total_count: Sequelize.INTEGER,
  coordinates: Sequelize.STRING,
  departement_code: Sequelize.INTEGER,
  state_code: Sequelize.INTEGER
});

module.exports = City;


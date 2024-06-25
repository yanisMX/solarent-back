const Sequelize = require('sequelize');
const sequelize = require('../sequelize');

const Department = sequelize.define('department', {
  code: {
    type: Sequelize.INTEGER,
    primaryKey: true
  },
  name: Sequelize.STRING,
  sun_rate: Sequelize.INTEGER
});

module.exports = Department;

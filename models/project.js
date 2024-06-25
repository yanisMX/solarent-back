const Sequelize = require('sequelize');
const sequelize = require('../sequelize');

const Project = sequelize.define('project', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  count: Sequelize.INTEGER,
  date: Sequelize.DATE,
  puissance: Sequelize.FLOAT,
  exploitation: Sequelize.STRING,
  city_code: Sequelize.STRING
});

module.exports = Project;

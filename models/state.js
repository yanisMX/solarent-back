const Sequelize = require('sequelize');
const sequelize = require('../sequelize');

const State = sequelize.define('state', {
  code: {
    type: Sequelize.INTEGER,
    primaryKey: true
  },
  name: Sequelize.STRING
});

module.exports = State;

const { Sequelize, DataTypes } = require("sequelize");
const sequelize = require("../sequelize");

const State = sequelize.define('state', {
  code: {
    type: DataTypes.INTEGER,
    primaryKey: true
  },
  name: 
  {
    type: DataTypes.STRING,
    allowNull: false
  }
},
{
  tableName: "state",
  timestamps: false,
}
);

module.exports = State;

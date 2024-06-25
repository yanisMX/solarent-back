const { Sequelize, DataTypes } = require("sequelize");
const sequelize = require("../sequelize");

const Department = sequelize.define(
  "Department",
  {
    code: {
      type: DataTypes.INTEGER,
      primaryKey: true,
    },
    name: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    sun_rate: {
      type: DataTypes.INTEGER,
      allowNull: false,
    },
  },
  {
    tableName: "department",
    timestamps: false,
  }
);

module.exports = Department;

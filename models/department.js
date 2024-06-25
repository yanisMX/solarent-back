const { Sequelize, DataTypes } = require("sequelize");
const sequelize = require("../sequelize");

const Department = sequelize.define(
  "Department",
  {
    departement_code: {
      type: DataTypes.INTEGER,
      primaryKey: true,
    },
    departement_name: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    departement_sun_rate: {
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

const { Sequelize, DataTypes } = require("sequelize");
const sequelize = require("../sequelize");

const City = sequelize.define(
  "City",
  {
    code_name: {
      type: DataTypes.STRING,
      primaryKey: true,
    },
    city_name: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    total_count: {
      type: DataTypes.INTEGER,
      allowNull: false,
    },
    coordinates: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    departement_code: {
      type: DataTypes.INTEGER,
      allowNull: false,
    },
    state_code: {
      type: DataTypes.INTEGER,
      allowNull: false,
    },
  },
  {
    tableName: "city",
    timestamps: false,
  }
);

module.exports = City;

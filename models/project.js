const { Sequelize, DataTypes } = require("sequelize");
const sequelize = require("../sequelize");

const Project = sequelize.define(
  "Project",
  {
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
    },
    count: {
      type: DataTypes.INTEGER,
      allowNull: false,
    },
    date: {
      type: DataTypes.DATE,
      allowNull: false,
    },
    puissance: {
      type: DataTypes.FLOAT,
      allowNull: false,
    },
    exploitation: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    city_code: {
      type: DataTypes.STRING,
      allowNull: false,
    },
  },
  {
    tableName: "project",
    timestamps: false,
  }
);

module.exports = Project;

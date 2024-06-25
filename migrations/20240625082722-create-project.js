"use strict";

module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.createTable("project", {
      id: {
        type: Sequelize.INTEGER,
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
      },
      count: {
        type: Sequelize.INTEGER,
        allowNull: true,
      },
      date: {
        type: Sequelize.DATE,
        allowNull: true,
      },
      puissance: {
        type: Sequelize.FLOAT,
        allowNull: true,
      },
      exploitation: {
        type: Sequelize.STRING,
        allowNull: true,
      },
      city_code: {
        type: Sequelize.STRING,
        allowNull: true,
        references: {
          model: "city", // nom de la table référencée
          key: "code_name",
        },
        onUpdate: "CASCADE",
        onDelete: "SET NULL",
      },
    });
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.dropTable("project");
  },
};

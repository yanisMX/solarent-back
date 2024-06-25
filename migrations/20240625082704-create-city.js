"use strict";
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable("city", {
      code_name: {
        type: Sequelize.STRING,
        allowNull: false,
        primaryKey: true,
      },
      name: {
        type: Sequelize.STRING,
      },
      total_count: {
        type: Sequelize.INTEGER,
      },
      coordinates: {
        type: Sequelize.STRING,
      },
      departement_code: {
        type: Sequelize.INTEGER,
      },
      state_code: {
        type: Sequelize.INTEGER,
      },
    });
  },
  async down(queryInterface, Sequelize) {
    await queryInterface.dropTable("city");
  },
};

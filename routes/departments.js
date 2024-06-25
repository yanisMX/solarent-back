const express = require("express");
const router = express.Router();
const Department = require("../models/department"); // Importez le modèle Sequelize pour les départements

// GET all departments
router.get("/", async (req, res) => {
  try {
    const departments = await Department.findAll();
    res.status(200).json(departments);
  } catch (error) {
    console.error(error);
    res
      .status(500)
      .send(
        "Une erreur est survenue lors de la récupération des départements."
      );
  }
});

// GET a single department by code
router.get("/:code", async (req, res) => {
  const code = req.params.code;
  try {
    const department = await Department.findOne({ where: { code: code } });
    if (department) {
      res.status(200).json(department);
    } else {
      res.status(404).send("Département non trouvé.");
    }
  } catch (error) {
    console.error(error);
    res
      .status(500)
      .send("Une erreur est survenue lors de la récupération du département.");
  }
});

module.exports = router;

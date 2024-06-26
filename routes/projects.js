const express = require("express");
const router = express.Router();
const Project = require("../models/project"); // Importez le modèle Sequelize

// GET all projets
router.get('/', async (req, res) => {
  try {
    const projects = await Project.findAll();
    res.status(200).json(projects);
  } catch (error) {
    console.log(projects);
    console.error(error);
    res
      .status(500)
      .send(
        'Une erreur est survenue lors de la récupération des projets.'
      );
  }
});

// GET a single projet by ID
router.get('/:id', async (req, res) => {
  const id = req.params.id;
  try {
    const project = await Project.findByPk(id);
    if (project) {
      res.status(200).json(project);
    } else {
      res.status(404).send('Projet non trouvé.');
    }
  } catch (error) {
    console.error(error);
    res.status(500).send('Une erreur est survenue lors de la récupération du projet.');
  }
});

module.exports = router;

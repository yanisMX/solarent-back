const express = require("express");
const router = express.Router();
const State = require("../models/state"); // Importez le modèle Sequelize pour les états

// GET all states
router.get('/', async (req, res) => {
  try {
    const states = await State.findAll();
    res.status(200).json(states);
  } catch (error) {
    console.error(error);
    res.status(500).send('Une erreur est survenue lors de la récupération des états.');
  }
});

// GET a single state by state_code
router.get('/:code', async (req, res) => {
  const state_code = req.params.state_code;
  try {
    const state = await State.findOne({ where: { code: state_code } });
    if (state) {
      res.status(200).json(state);
    } else {
      res.status(404).send('État non trouvé.');
    }
  } catch (error) {
    console.error(error);
    res.status(500).send('Une erreur est survenue lors de la récupération de l\'état.');
  }
});

module.exports = router;

const express = require('express');
const router = express.Router();
const City = require('../models/city'); // Importez le modèle Sequelize pour les villes

// GET all cities
router.get('/cities', async (req, res) => {
  try {
    const cities = await City.findAll();
    res.status(200).json(cities);
  } catch (error) {
    console.error(error);
    res.status(500).send('Une erreur est survenue lors de la récupération des villes.');
  }
});

// GET a single city by code_name
router.get('/cities/:code_name', async (req, res) => {
  const code_name = req.params.code_name;
  try {
    const city = await City.findOne({ where: { code_name: code_name } });
    if (city) {
      res.status(200).json(city);
    } else {
      res.status(404).send('Ville non trouvée.');
    }
  } catch (error) {
    console.error(error);
    res.status(500).send('Une erreur est survenue lors de la récupération de la ville.');
  }
});

module.exports = router;
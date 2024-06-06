const express = require('express');
const router = express.Router();
const pool = require('../db');

// GET all cities
router.get('/cities', (req, res) => {
  pool.query('SELECT * FROM city', (error, results) => {
    if (error) {
      throw error;
    }
    res.status(200).json(results.rows);
  });
});

// GET a single city by code_name
router.get('/cities/:code_name', (req, res) => {
  const code_name = req.params.code_name;
  pool.query('SELECT * FROM city WHERE code_name = $1', [code_name], (error, results) => {
    if (error) {
      throw error;
    }
    res.status(200).json(results.rows);
  });
});

module.exports = router;
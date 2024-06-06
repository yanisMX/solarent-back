const express = require('express');
const router = express.Router();
const pool = require('../db');

// GET all states
router.get('/states', (req, res) => {
  pool.query('SELECT * FROM state', (error, results) => {
    if (error) {
      throw error;
    }
    res.status(200).json(results.rows);
  });
});

// GET a single state by state_code
router.get('/states/:state_code', (req, res) => {
  const state_code = req.params.state_code;
  pool.query('SELECT * FROM state WHERE state_code = $1', [state_code], (error, results) => {
    if (error) {
      throw error;
    }
    res.status(200).json(results.rows);
  });
});

module.exports = router;
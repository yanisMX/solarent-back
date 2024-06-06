const express = require('express');
const router = express.Router();
const pool = require('../db');

// GET all departments
router.get('/departments', (req, res) => {
  pool.query('SELECT * FROM department', (error, results) => {
    if (error) {
      throw error;
    }
    res.status(200).json(results.rows);
  });
});

// GET a single department by code
router.get('/departments/:code', (req, res) => {
  const code = req.params.code;
  pool.query('SELECT * FROM department WHERE code = $1', [code], (error, results) => {
    if (error) {
      throw error;
    }
    res.status(200).json(results.rows);
  });
});

module.exports = router;
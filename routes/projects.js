const express = require('express');
const router = express.Router();
const pool = require('../db');

router.get('/projects', (req, res) => {
  pool.query('SELECT * FROM project', (error, results) => {
    if (error) {
      throw error;
    }
    res.status(200).json(results.rows);
  });
});

router.get('/projects/:id', (req, res) => {
  const id = req.params.id;
  pool.query('SELECT * FROM project WHERE id = $1', [id], (error, results) => {
    if (error) {
      throw error;
    }
    res.status(200).json(results.rows);
  });
});

module.exports = router;

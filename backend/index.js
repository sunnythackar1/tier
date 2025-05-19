const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');

const app = express();
app.use(cors());
app.use(express.json());

const pool = new Pool({
  host: 'db',
  user: 'postgres',
  password: 'postgres',
  database: 'tasks',
});

app.get('/api/tasks', async (req, res) => {
  const result = await pool.query('SELECT * FROM tasks');
  res.json(result.rows);
});

app.post('/api/tasks', async (req, res) => {
  const { text } = req.body;
  await pool.query('INSERT INTO tasks (text) VALUES ($1)', [text]);
  res.sendStatus(201);
});

app.listen(5000, () => console.log('Backend running on port 5000'));

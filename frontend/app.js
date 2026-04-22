const express = require('express');
const axios = require('axios');
const path = require('path');
const app = express();

const API_URL = process.env.API_URL || "http://localhost:8000";
const PORT = process.env.PORT || 3000; // missing PORT declaration added back

const axiosInstance = axios.create({ timeout: 5000 });

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
  res.status(200).json({ message: "API is running" });
});

app.post('/submit', async (req, res) => {
  try {
    const response = await axiosInstance.post(`${API_URL}/jobs`, req.body);
    res.json(response.data);
  } catch (err) {
    console.error(err.message);
    res.status(500).json({ error: err.message || "Internal Server Error" });
  } // ✅ closing } for catch added back
});

app.get('/status/:id', async (req, res) => {
  try {
    const { id } = req.params;

    if (!id) {
      return res.status(400).json({ error: "ID is required" });
    }

    const response = await axiosInstance.get(`${API_URL}/jobs/${id}`);
    res.json(response.data);
  } catch (err) {
    console.error(err.message);
    res.status(500).json({ error: err.message || "Internal Server Error" });
  }
});

app.use((req, res) => {
  res.status(404).json({ error: "Route not found" });
});

app.listen(PORT, () => {
  console.log(`Frontend running on port ${PORT}`);
});
const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();

const API_URL = process.env.API_URL || "http://api:8000"; // use service name in Docker
const PORT = process.env.PORT || 3000;

const axiosInstance = axios.create({
  timeout: 5000
});

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Health-style root endpoint (frontend check)
app.get('/', (req, res) => {
  res.status(200).json({ message: "Frontend is running" });
});

// Submit job (primary endpoint)
app.post('/jobs', async (req, res) => {
  try {
    const response = await axiosInstance.post(`${API_URL}/jobs`, req.body);
    return res.status(200).json(response.data);
  } catch (err) {
    console.error("POST /jobs error:", err.message);
    return res.status(500).json({ error: "Failed to submit job" });
  }
});

// Backward compatibility (optional but safe)
app.post('/submit', async (req, res) => {
  try {
    const response = await axiosInstance.post(`${API_URL}/jobs`, req.body);
    return res.status(200).json(response.data);
  } catch (err) {
    console.error("POST /submit error:", err.message);
    return res.status(500).json({ error: "Failed to submit job" });
  }
});

// Get job status (standard route)
app.get('/jobs/:id', async (req, res) => {
  try {
    const { id } = req.params;

    if (!id) {
      return res.status(400).json({ error: "ID is required" });
    }

    const response = await axiosInstance.get(`${API_URL}/jobs/${id}`);
    return res.status(200).json(response.data);
  } catch (err) {
    console.error("GET /jobs/:id error:", err.message);
    return res.status(500).json({ error: "Failed to fetch job status" });
  }
});

// Alias route (for UI compatibility)
app.get('/status/:id', async (req, res) => {
  try {
    const { id } = req.params;

    if (!id) {
      return res.status(400).json({ error: "ID is required" });
    }

    const response = await axiosInstance.get(`${API_URL}/jobs/${id}`);
    return res.status(200).json(response.data);
  } catch (err) {
    console.error("GET /status/:id error:", err.message);
    return res.status(500).json({ error: "Failed to fetch job status" });
  }
});

// 404 handler (must be last)
app.use((req, res) => {
  res.status(404).json({ error: "Route not found" });
});

app.listen(PORT, () => {
  console.log(`Frontend running on port ${PORT}`);
});
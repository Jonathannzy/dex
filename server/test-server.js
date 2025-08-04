const express = require('express');
const app = express();

app.use(express.json());

app.get('/health', (req, res) => {
  res.json({ status: 'OK', message: 'Test server is running' });
});

app.get('/', (req, res) => {
  res.json({ message: 'Cosmic Explorers Test Server' });
});

const PORT = 3001;

app.listen(PORT, () => {
  console.log(`Test server running on port ${PORT}`);
});
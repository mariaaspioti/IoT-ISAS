import express from 'express';
import axios from 'axios';

const app = express();
const port = 3000;

// Orion Context Broker URL
const orionUrl = 'http://150.140.186.118:1026/v2/entities';
const fiwareService = 'ISAS';
const fiwareServicePath = '/test';
const getHeaders = {
    'Fiware-Service': fiwareService,
    'Fiware-ServicePath': fiwareServicePath,
};

//
app.get('/', (req, res) => {
    res.send('Go to /entities to fetch entities from Orion Context Broker');
});

// Endpoint to fetch entities from Orion Context Broker
app.get('/entities', async (req, res) => {
    try {
        const queryParams = req.query;
        const response = await axios.get(orionUrl, {
             headers: getHeaders,
             params: queryParams
            });
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching entities:', error);
        res.status(500).send('Error fetching entities');
    }
});

// Serve static files (e.g., HTML, CSS, JS)
// app.use(express.static('public'));

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
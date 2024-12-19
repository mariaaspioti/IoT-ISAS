import express from 'express';
import axios from 'axios';

import cors from 'cors';

const app = express();
const indexRouter = express.Router();

// Orion Context Broker URL
const orionUrl = 'http://150.140.186.118:1026/v2/entities';
const fiwareService = 'ISAS';
const fiwareServicePath = '/test';
const getHeaders = {
    'Fiware-Service': fiwareService,
    'Fiware-ServicePath': fiwareServicePath,
};

// Enable CORS
app.use(cors({ origin: 'http://localhost:3000' })); // allow requests from this, React development server

// Parse JSON bodies (as sent by API clients)
app.use(express.json()); 

// DEBUG
// Sample API endpoint
app.get('/api/data', (req, res) => {
    // change the value every second
    let dx = Math.random() * 0.01 - 0.05;
    const responseObject = {
        data: [
            { lat: 51.505 + dx, lng: -0.09, msg: 'id 1' },
            { lat: 51.505, lng: -0.09 + dx, msg: 'id 2' },
        ],
        message: 'Hello from the server!',
    };
    res.json(responseObject);
});

//
app.use('/', indexRouter);

// Serve static files (e.g., HTML, CSS, JS)
// app.use(express.static('public'));


// Endpoint to fetch entities from Orion Context Broker
indexRouter.get('/entities', async (req, res) => {
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

//
indexRouter.get('/', (req, res) => {
    res.send('Go to /entities to fetch entities from Orion Context Broker');
});

// handle errors
app.use((req, res) => {
    res.status(404).send('404: Page not Found');
});

export {app as application};
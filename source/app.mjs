import express from 'express';
import axios from 'axios';

import cors from 'cors';

// 
const app = express();

// Routers
const indexRouter = express.Router();
import { apiRoutes } from './routes/apiRoutes.js';


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

//
app.use('/', indexRouter);
app.use('/api', apiRoutes);


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
import express from 'express';
import axios from 'axios';
import http from 'http';
import cors from 'cors';
import {Server as SocketIOServer} from 'socket.io';

// 
const app = express();

// Routers
const indexRouter = express.Router();
import { apiRoutes } from './routes/apiRoutes.js';
import { startAlertPolling } from './util/orionPolling.js';


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

// ------------------------------
//  Orion Polling
// ------------------------------

// Create an HTTP server from the Express app
const server = http.createServer(app);

// Create a Socket.IO server and attach it to the HTTP server
const io = new SocketIOServer(server, {
  cors: {
    origin: 'http://localhost:3000',
    methods: ["GET", "POST"]
  }
});

// When a client connects via Socket.IO
io.on('connection', (socket) => {
  console.log('A client connected:', socket.id);
  
  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
  });
});

// Start polling Orion for alert data and emit new alerts via Socket.IO
startAlertPolling(io, 3000);

// ---
// Export the HTTP server for use in index.mjs
// ---

export { server as application};
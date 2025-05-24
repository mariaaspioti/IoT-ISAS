import express from 'express';
import axios from 'axios';
import http from 'http';
// import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';
import {Server as SocketIOServer} from 'socket.io';

// 
const app = express();

// Routers
const indexRouter = express.Router();
import { apiRoutes } from './routes/apiRoutes.js';
import { startAlertPolling, startNFCPolling } from './utils/orionPolling.js';



// Orion Context Broker URL
const orionUrl = 'http://150.140.186.118:1026/v2/entities';
const fiwareService = 'ISAS';
const fiwareServicePath = '/test';
const getHeaders = {
    'Fiware-Service': fiwareService,
    'Fiware-ServicePath': fiwareServicePath,
};

// Enable CORS
// app.use(cors({ origin: 'http://localhost:3000' })); // allow requests from this, React development server

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
// indexRouter.get('/', (req, res) => {
//     res.send('Go to /entities to fetch entities from Orion Context Broker');
// });
// Serve static files from the React app
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
app.use(express.static(path.join(__dirname, 'frontend', 'build')));

// Catch-all handler to serve React's index.html for any other routes
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend', 'build', 'index.html'));
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
    methods: ["GET", "POST"],
    credentials: true
  },
  transports: ['websocket', 'polling'],
});

// When a client connects via Socket.IO
io.on('connection', (socket) => {
  // console.log('A client connected:', socket.id);
  
  socket.on('disconnect', () => {
    // console.log('Client disconnected:', socket.id);
  });
});

// Start polling Orion for alert data and emit new alerts via Socket.IO
const stopAlertPolling = startAlertPolling(io, 3000);

// Start polling Orion for NFC data and emit new data via Socket.IO with a limit of 50 entities
const stopNFCPolling = startNFCPolling(io, 3000, 100);


// Handle SIGINT signal (Ctrl+C)
process.on('SIGINT', () => {
  console.log('Received SIGINT. Shutting down gracefully...');
  stopAlertPolling();
  stopNFCPolling();
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});

// ---
// Export the HTTP server for use in index.mjs
// ---

export { server as application};
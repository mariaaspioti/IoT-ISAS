// import dotenv from 'dotenv';

// if (process.env.NODE_ENV !== 'production') {
//     console.log('Loading .env file');
//     dotenv.config();
// }

import { application } from './app.mjs';

const port = process.env.PORT || '3001';

const server = application.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
    // console.log(`Server running in ${process.env.NODE_ENV} mode`);
});

const shutdown = () => {
    console.log('Closing http server.');
    server.close(() => {
       console.log('Http server closed.');
    });
 };

process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);
process.on('SIGUSR2', shutdown); 
 
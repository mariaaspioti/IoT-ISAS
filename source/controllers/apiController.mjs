import fs from 'fs';
import axios from 'axios';
// import express from 'express';

// Orion Context Broker URL
const orionUrl = 'http://150.140.186.118:1026/v2/entities';
const fiwareService = 'ISAS';
const fiwareServicePath = '/test';
const getHeaders = {
    'Fiware-Service': fiwareService,
    'Fiware-ServicePath': fiwareServicePath,
};

let getData = (req, res) => {
    // DEBUG:
    // change the value every second
    // let dx = Math.random() * 0.01 - 0.05;
    // const responseObject = {
    //     data: [
    //         { lat: 51.505 + dx, lng: -0.09, msg: 'id 1' },
    //         { lat: 51.505, lng: -0.09 + dx, msg: 'id 2' },
    //     ],
    //     message: 'Hello from the server!',
    // };
    // res.json(responseObject);

    // get the coordinates from the Orion Context Broker
    let MSCPaskCoords = `?type=Building&q=name==R%26D`;
    let MSCPaskUrl = orionUrl + MSCPaskCoords;
    axios.get(MSCPaskUrl, {
        headers: getHeaders
    })
    .then((response) => {
        let MSCPcoords = response.data[0].location.value.coordinates[0];
        
        let responseObject = {
            data: [],
            message: 'Hello from the server!',
        };
        for (let i = 0; i < MSCPcoords.length; i++) {
            let coord = MSCPcoords[i];
            let dataPoint = {
                lat: coord[1],
                lng: coord[0],
                msg: `MSCP ${i + 1}`,
            };
            responseObject.data.push(dataPoint);
        }

        res.json(responseObject);
    })
}

let saveCoordinates = (req, res) => {
    const newCoord = req.body; // Expect { lat: number, lng: number }

    // Read existing coordinates from file
    const filePath = './coordinates.json';
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err && err.code !== 'ENOENT') {
            return res.status(500).send('Error reading coordinates file');
        }

        // Parse existing data or initialize an empty array
        const coordinates = data ? JSON.parse(data) : [];

        // Add the new coordinate
        coordinates.push(newCoord);

        // Write updated data back to the file
        fs.writeFile(filePath, JSON.stringify(coordinates, null, 2), (writeErr) => {
            if (writeErr) {
                return res.status(500).send('Error writing to coordinates file');
            }
            res.status(200).send('Coordinate saved successfully');
        });
    });
};

export { getData, saveCoordinates };
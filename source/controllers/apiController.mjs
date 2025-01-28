import fs from 'fs';
import axios from 'axios';
// import express from 'express';
import * as turf from '@turf/turf';

// Orion Context Broker URL
const orionUrl = 'http://150.140.186.118:1026/v2/entities';
const fiwareService = 'ISAS';
const fiwareServicePath = '/test';
const getHeaders = {
    'Fiware-Service': fiwareService,
    'Fiware-ServicePath': fiwareServicePath,
};

let getData = (req, res) => {
    // get the coordinates from the Orion Context Broker for a specific building
    let MSCPaskCoords = `?type=Building&q=name==Waste Water Treatment Building`;
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

let getAllData = (req, res) => {
    // get the coordinates from the Orion Context Broker for all buildings
    let allCoords = `?type=Building`;
    let allUrl = orionUrl + allCoords;
    axios.get(allUrl, {
        headers: getHeaders
    })
    .then((response) => {
        let responseObject = {
            data: [],
            message: 'Hello from the server!',
        };
        for (let i = 0; i < response.data.length; i++) {
            let coords = response.data[i].location.value.coordinates[0];
            for (let j = 0; j < coords.length; j++) {
                let coord = coords[j];
                let dataPoint = {
                    lat: coord[1],
                    lng: coord[0],
                    msg: `${response.data[i].name.value} ${j + 1}`,
                };
                responseObject.data.push(dataPoint);
            }
        }

        res.json(responseObject);
    })
}

let getDeviceLocationData = (req, res) => {
    // get the coordinates from the Orion Context Broker for a specific device
    const device_id = req.params.id;
    let deviceCoords = `/${device_id}/attrs/location`;
    let deviceUrl = orionUrl + deviceCoords;
    axios.get(deviceUrl, {
        headers: getHeaders
    })
    .then((response) => {
        let coord = response.data.value.coordinates;
        
        let responseObject = {
            data: [{
                lat: coord[1],
                lng: coord[0],
                msg: device_id,
            }],
            message: 'Hello from the server!',
        };

        res.json(responseObject);
    })
}

let getAllDevicesLocationData = (req, res) => {
    // get the coordinates from the Orion Context Broker for all devices
    let allDevices = `?type=Device`;
    let allDevicesUrl = orionUrl + allDevices;
    axios.get(allDevicesUrl, {
        headers: getHeaders
    })
    .then((response) => {
        let responseObject = {
            data: [],
            message: 'Hello from the server!',
        };
        for (let i = 0; i < response.data.length; i++) {
            let coord = response.data[i].location.value.coordinates;
            let dataPoint = {
                lat: coord[1],
                lng: coord[0],
                msg: response.data[i].id,
            };
            responseObject.data.push(dataPoint);
        }

        res.json(responseObject);
    })
}

let getAllDevicesControlledAssets = async (req, res) => {
    // Get all devices from the Orion Context Broker
    let allDevices = `?type=Device`;
    let allDevicesUrl = orionUrl + allDevices;

    try {
        const deviceResponse = await axios.get(allDevicesUrl, { headers: getHeaders });
        let responseObject = {
            data: [],
            message: 'Hello from the server!',
        };

        // Collect promises for fetching person data
        let promises = deviceResponse.data.map(async (device) => {
            let controlledAsset = device.controlledAsset.value;
            // Fetch person details for the first controlled asset
            let personUrl = orionUrl + `/${controlledAsset[0]}`;
            const personResponse = await axios.get(personUrl, { headers: getHeaders });

            // Validate that the person `hasDevices` the device
            let hasDevices = personResponse.data.hasDevices.value;
            if (hasDevices.includes(device.id)) {
                let dataPoint = {
                    person_name: personResponse.data.name.value,
                    person_id: personResponse.data.id,
                    device_id: device.id,
                };
                responseObject.data.push(dataPoint);
            }
        });

        // Wait for all person-related promises to complete
        await Promise.all(promises);

        // Send the populated responseObject after all data is fetched
        res.json(responseObject);
    } catch (error) {
        console.error('Error fetching data:', error);
        res.status(500).json({ error: 'An error occurred while fetching data' });
    }
};

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

let getFacilities = (req, res) => {
    // get the coordinates from the Orion Context Broker for all facilities
    let allFacilities = `?type=Facility`;
    let allFacilitiesUrl = orionUrl + allFacilities;
    axios.get(allFacilitiesUrl, {
        headers: getHeaders
    })
    .then((response) => {
        let facilities = response.data;
        res.json({ data: facilities });
    })
}

// Helper function for array comparison
function arraysEqual(a, b) {
    return a.length === b.length && a.every((val, i) => val === b[i]);
}

const findFacilityContainingPoint = (point, facilities) => {
    try {
        return facilities.find(f => {
            const coords = f.bounds;
            // Add validation
            if (!coords || coords.length < 3) {
                console.warn('Invalid polygon for facility:', f.name);
                return false;
            }
            
            // Convert coordinates and close polygon
            const formattedCoords = coords.map(coord => [coord[0], coord[1]]);
            // console.log('Formatted coordinates:', formattedCoords);
            if (!arraysEqual(formattedCoords[0], formattedCoords[formattedCoords.length-1])) {
                formattedCoords.push(formattedCoords[0]);
            }
            
            const polygon = turf.polygon([formattedCoords]);
            const isInPolygon = turf.booleanPointInPolygon(point, polygon);
            
            // Optional: Uncomment for debugging
            // console.log(`Checking facility ${f.name}:`, isInPolygon);
            
            return isInPolygon;
        });
    } catch (error) {
        console.error('Error finding facility:', error);
        return null;
    }
};

let findCurrentFacilities = async (req, res) => {
    try {
        const { coordinates } = req.body;
        
        if (!coordinates?.length) {
            return res.status(400).json({ error: 'Invalid coordinates data' });
        }

        // Get facilities
        const response = await axios.get(`${orionUrl}?type=Building`, {
            headers: getHeaders
        });
        
        // Map to proper structure
        const facilities = response.data.map(f => ({
            id: f.id,
            name: f.name.value,
            bounds: f.location.value.coordinates[0]
        }));

        // Process all coordinates in parallel
        const enrichedCoordinates = await Promise.all(coordinates.map(async (loc) => {
            const point = turf.point([loc.lng, loc.lat]);
            const facility = findFacilityContainingPoint(point, facilities);
            return {
                name: facility?.name || 'Outside',
                id: facility?.id || 'Outside',
            };
        }));

        res.json({ data: enrichedCoordinates });
    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ error: 'Server error' });
    }
};

export { getData, getAllData, getDeviceLocationData, getAllDevicesLocationData, 
    getAllDevicesControlledAssets, saveCoordinates, getFacilities, findCurrentFacilities
 };
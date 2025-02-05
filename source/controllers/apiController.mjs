import fs from 'fs';
import axios from 'axios';
// import express from 'express';
// import * as turf from '@turf/turf';
import * as stateController from '../controllers/stateController.mjs';

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
    // let deviceCoords = `/${device_id}/attrs/location`;
    let deviceUrl = orionUrl;
    axios.get(deviceUrl, {
        headers: getHeaders,
        params: {
            id: device_id,
            attrs: 'location, name'
        }
    })
    .then((response) => {
        let coord = response.data.value.coordinates;
        let device_name = response.data.name.value;
        
        let responseObject = {
            data: [{
                lat: coord[1],
                lng: coord[0],
                id: device_id,
                name: device_name,
            }],
            message: 'Hello from the server!',
        };

        res.json(responseObject);
    })
}

let getAllDevicesLocationData = (req, res) => {
    // get the coordinates from the Orion Context Broker for all devices
    // get the location and the name of the devices
    const allDevices = `?type=Device`;
    const locationAndName = `&attrs=location,name,controlledAsset`;
    const allDevicesUrl = orionUrl + allDevices + locationAndName;
    axios.get(allDevicesUrl, {
        headers: getHeaders,
    })
    .then((response) => {
        let responseObject = {
            data: [],
            message: 'Hello from the server!',
        };
        for (let i = 0; i < response.data.length; i++) {
            let coord = response.data[i].location.value.coordinates;
            let device_id = response.data[i].id;
            let device_name = response.data[i]?.name.value;
            let device_controlledAsset = response.data[i].controlledAsset.value;
            let dataPoint = {
                lat: coord[1],
                lng: coord[0],
                id: device_id,
                name: device_name,
                controlledAsset: device_controlledAsset,
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
            let controlledAssetUrl = orionUrl + `/${controlledAsset[0]}`;
            const controlledAssetResponse = await axios.get(controlledAssetUrl, { headers: getHeaders });

            // Check if the controlled asset is a person
            if (controlledAssetResponse.data.type === 'Person') {
                let dataPoint = {
                    device_id: device.id,
                    person_id: controlledAssetResponse.data.id,
                    person_name: controlledAssetResponse.data.name.value,
                    isIndoors: controlledAssetResponse.data.isIndoors ? controlledAssetResponse.data.isIndoors.value : null,
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

let getFacilities = async (req, res) => {
  try {
    const response = await axios.get(`${orionUrl}?type=Building`, {
      headers: getHeaders,
      params: {
        attrs: 'name,location'
        }
    });
    res.json({ data: response.data });
  } catch (error) {
    console.error('Facilities error:', error);
    res.status(500).json({ error: 'Failed to fetch facilities' });
  }
};

let findCurrentFacilities = async (req, res) => {
  try {
    const { coordinates } = req.body;
    
    if (!coordinates?.length) {
      return res.status(400).json({ error: 'Invalid coordinates data' });
    }

    const facilityResponse = await axios.get(`${orionUrl}?type=Building`, {
      headers: getHeaders
    });
    
    const inOrderIndexesCurrentFacilities = await stateController.processFacilities(
        coordinates, facilityResponse.data);
    await stateController.determineInsideOutsideFacilities(inOrderIndexesCurrentFacilities);
    const enriched = inOrderIndexesCurrentFacilities;

    res.json({ data: enriched });
    

    // as a secondary task, update the persons' currentFacility attribute
    // rename the enriched data to match the expected structure
    await stateController.updateCurrentFacilityForPersons(enriched.map(data => ({
      lat: data.lat,
      lng: data.lng,
      facility_id: data.id,
      facility_name: data.name
    })));

    // console.log('Was a facility id found?\n=======');
    // enriched.forEach((facility) => {
    //     if (facility.id) {
    //         console.log('Yes:', facility.id);
    //     } else {
    //         console.log('No:', facility.id);
    //     }
    //     });
    // console.log('=======\n');
    // // validate the correct update of the persons' currentFacility attribute
    // const persons = await axios.get(`${orionUrl}?type=Person`, {
    //   headers: getHeaders
    // });
    // // console.log('Persons:', persons.data);
    
  } catch (error) {
    console.error('Location error:', error);
    res.status(500).json({ error: 'Facility lookup failed' });
  }
};

let getDoorsLocations = async (req, res) => {
    try {
        const response = await axios.get(`${orionUrl}?type=Door`, {
        headers: getHeaders,
        params: {
            attrs: 'location'
            }
        });
        res.json({ data: response.data });
    } catch (error) {
        console.error('Doors error:', error);
        res.status(500).json({ error: 'Failed to fetch doors' });
    }
}

let handleSOSAlert = (req, res) => {
    try {
        console.log('SOS Alert received:', req.body);
        res.json({ message: 'SOS Alert received' });

        // record it in a file
        const filePath = '../sos-alerts.json';
        const alert = req.body;
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err && err.code !== 'ENOENT') {
                console.error('Error reading SOS alerts file:', err);
                return;
            }

            const alerts = data ? JSON.parse(data) : [];
            alerts.push(alert);

            fs.writeFile(filePath, JSON.stringify(alerts, null, 2), (writeErr) => {
                if (writeErr) {
                    console.error('Error writing to SOS alerts file:', writeErr);
                }
            });
        });
    } catch (error) {
        console.error('SOS Alert error:', error);
        res.status(500).json({ error: 'Failed to handle SOS alert' });
    }
};

export { getData, getAllData, getDeviceLocationData, getAllDevicesLocationData, 
    getAllDevicesControlledAssets, saveCoordinates, getFacilities, findCurrentFacilities,
    getDoorsLocations, handleSOSAlert
 };
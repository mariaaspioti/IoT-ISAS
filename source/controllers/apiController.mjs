import fs from 'fs';
import axios from 'axios';
// import express from 'express';
// import * as turf from '@turf/turf';
import * as stateController from '../controllers/stateController.mjs';
import * as maintenanceController from '../controllers/maintenanceController.mjs';
import * as cameraController from '../controllers/cameraController.mjs';
// import * as smartlockController from '../controllers/smartlockController.mjs'
// Orion Context Broker URL
const orionUrl = 'http://150.140.186.118:1026/v2/entities';
const fiwareService = 'ISAS';
const fiwareServicePath = '/test';
const getHeaders = {
    'Fiware-Service': fiwareService,
    'Fiware-ServicePath': fiwareServicePath,
};
const patchHeaders = {
    'Fiware-Service': fiwareService,
    'Fiware-ServicePath': fiwareServicePath,
    'Content-Type': 'application/json',
}


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

let getDeviceData = (req, res) => {
    // get the Entity data from the Orion Context Broker for a specific device given an :id
    const deviceId = req.params.id;
    axios.get(orionUrl + `/${deviceId}`, {
        headers: getHeaders
    })
    .then((response) => {
        res.json({
            success: true,
            data: response.data
        });
    })
    .catch((error) => {
        console.error('Error fetching device data in getDeviceData:');
        res.status(500).json({ error: 'Failed to fetch device data' });
    });
}

let getDeviceDataFromName = (req, res) => {
    // get the Entity data from the Orion Context Broker for a specific device given a :name
    const deviceName = req.params.name;
    const queryParams = {
        type: 'Device',
        q: `name==${deviceName}`,
    };
    axios.get(orionUrl, {
        headers: getHeaders,
        params: queryParams
    })
    .then((response) => {
        res.json({
            success: true,
            data: response.data
        });
    })
    .catch((error) => {
        console.error('Error fetching device data in getDeviceDataFromName:', error);
        res.status(500).json({ error: 'Failed to fetch device data' });
    });
}

let getDeviceLocationData = (req, res) => {
    // get the coordinates from the Orion Context Broker for a specific device
    const device_id = req.params.id;
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
    const allDevices = `?type=Device&q=deviceCategory==meter`;
    const locationAndName = `&attrs=location,name,controlledAsset`;
    const queryLimit = `&limit=1000`;
    const allDevicesUrl = orionUrl + allDevices + locationAndName + queryLimit;
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
                    person_role: controlledAssetResponse.data.role.value,
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

let getAllFacilities = async (req, res) => {
    try {
        const response = await axios.get(`${orionUrl}?type=Building`, {
            headers: getHeaders
        });
        res.json({ data: response.data });
    } catch (error) {
        console.error('Facilities error:', error);
        res.status(500).json({ error: 'Failed to fetch facilities' });
    }
};

let getFacilitiesNameAndLocation = async (req, res) => {
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

let getFacilityLocationData = async (req, res) => {
    try {
        const facilityId = req.params.id;
        const response = await axios.get(`${orionUrl}/${facilityId}`, {
            headers: getHeaders,
            params: {
                options: 'keyValues',
                attrs: 'location'
            }
        });

        if (!response.data.location?.coordinates) {
            return res.status(404).json({ error: 'Coordinates not found' });
        }

        const coordinates = response.data.location.coordinates[0]
            .map(([lng, lat]) => [lat, lng ]);

        res.json(coordinates);
    } catch (error) {
        console.error('Coordinate fetch error in getFacilityLocationData:');
        res.status(500).json({ error: 'Failed to fetch facility location' });
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

let getPersonData = async (req, res) => {
    try {
        const personId = req.params.id;
        const response = await axios.get(`${orionUrl}/${personId}`, {
            headers: getHeaders
        });
        res.json({ data: response.data });
    } catch (error) {
        console.error('Person error:', error);
        res.status(500).json({ error: 'Failed to fetch person data' });
    }
}

let getAllPeopleData = async (req, res) => {
    try {
        const response = await axios.get(`${orionUrl}?type=Person`, {
            headers: getHeaders
        });
        res.json({ data: response.data });
    } catch (error) {
        console.error('People error:', error);
        res.status(500).json({ error: 'Failed to fetch people' });
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

let handleMaintenanceSchedule = async (req, res) => {
    try {
        const sampleReservation = { // check id
            type: 'MaintenanceReservation',
            building: {
                type: 'Relationship',
                value: req.body.buildingId
            },
            startTime: {
                type: 'DateTime',
                value: req.body.start
            },
            endTime: {
                type: 'DateTime',
                value: req.body.end
            },
            exemptPersonnel: {
                type: 'Relationship',
                value: req.body.exemptPersonnel
            },
            status: {
                type: 'Text',
                value: 'scheduled'
            }
        };

        const startDateTime = req.body.start;
        const endDateTime = req.body.end;
        const status = 'scheduled';
        const description = req.body?.description || 'No description';
        const dateCreated = new Date().toISOString();

        const buildingReservedCBId = req.body.buildingId;
        // since the buildingId is a context broker id, we need to fetch the SQL id
        const buildingReserved = await maintenanceController.getFacilityByCBId(buildingReservedCBId);
        const buildingReservedId = buildingReserved.facility_id;

        const peopleCBIds = req.body.exemptPersonnel;
        // since the peopleIds are context broker ids, we need to fetch the SQL ids
        const peopleArray = await Promise.all(peopleCBIds.map(async (personCBId) => {
            const person =  await maintenanceController.getPersonByCBId(personCBId);
            return person
        }));
        const peopleIds = peopleArray.map(person => person.person_id);
        const peopleNames = peopleArray.map(person => person.name);

        const maintenanceRecord = {
            startTime: startDateTime,
            endTime: endDateTime,
            dateCreated,
            status,
            description,
            peopleIds,
            facilityId: buildingReservedId
        };

        // Insert maintenance record into the database
        maintenanceController.insertMaintenanceRecord(maintenanceRecord, (err) => {
            if (err) {
                console.error('Error inserting maintenance record:', err);
                res.status(500).json({ error: 'Failed to create maintenance reservation' });
            }
            const maintenance = {
                startTime: startDateTime,
                endTime: endDateTime,
                dateCreated,
                status,
                description,
                peopleNames,
                peopleCBIds,
                facilityName: buildingReserved.name,
                facilityId: buildingReservedCBId
            };
            res.status(201).json(maintenance);
        });
    } catch (error) {
        res.status(500).json({ error: 'Failed to create maintenance reservation' });
    }
};

let getScheduledMaintenances = async (req, res) => {
    try {
        maintenanceController.getScheduledMaintenances(async (err, maintenances) => {
            if (err) {
                console.error('Error fetching scheduled maintenance:', err);
                res.status(500).json({ error: 'Failed to fetch scheduled maintenance' });
            }
            // maintenances.facility_id and maintenances.person_ids are SQL ids, not context broker ids
            // we need to fetch the context broker ids
            const maintenancePromises = maintenances.map(async (maintenance) => {
                const facility = await maintenanceController.getFacilityById(maintenance.facility_id);
                const facilityCBId = facility.context_broker_id;
                const facilityName = facility.name;
                // maintenance.person_ids is a string of comma-separated SQL ids if it exists
                if (!maintenance.person_ids) {
                    return {
                        id: maintenance.maintenance_id,
                        startTime: maintenance.startTime,
                        endTime: maintenance.endTime,
                        dateCreated: maintenance.date_created,
                        status: maintenance.status,
                        description: maintenance.description,
                        peopleNames: [],
                        peopleIds: [],
                        facilityName,
                        facilityId: facilityCBId
                    }
                }
                const personIds = maintenance.person_ids.split(',');
                const peoplePromises = personIds.map(async (personId) => {
                    const person = await maintenanceController.getPersonById(personId);
                    return person
                });
                const people = await Promise.all(peoplePromises);
                const peopleCBIds = people.map(person => person.context_broker_id);
                const peopleNames = people.map(person => person.name);
                return {
                    id: maintenance.maintenance_id,
                    startTime: maintenance.startTime,
                    endTime: maintenance.endTime,
                    dateCreated: maintenance.date_created,
                    status: maintenance.status,
                    description: maintenance.description,
                    peopleNames,
                    peopleIds: peopleCBIds,
                    facilityName,
                    facilityId: facilityCBId
                }
            });
            const enrichedMaintenances = await Promise.all(maintenancePromises);

            res.json({ data: enrichedMaintenances });
        });
    } catch (error) {
        console.error('Scheduled maintenance error in getScheduledMaintenances:', error);
        res.status(500).json({ error: 'Failed to fetch scheduled maintenance' });
    }
};

let updateMaintenanceStatus = async (req, res) => {
    try {
        const maintenanceId = req.params.id;
        const { status } = req.body;
        maintenanceController.updateMaintenanceStatus(maintenanceId, status, (err) => {
            if (err) {
                console.error('Error updating maintenance status:', err);
                res.status(500).json({ error: 'Failed to update maintenance status' });
            }
            res.json({ message: 'Maintenance status updated successfully' });
        });
    } catch (error) {
        console.error('Maintenance status update error:', error, 'in updateMaintenanceStatus');
        res.status(500).json({ error: 'Failed to update maintenance status' });
    }
};

let checkAccessAuthorization = async (req, res) => {
    const { person, building } = req.query;

    try {
        //do nothing

    } catch (error) {
    res.status(500).json({ authorized: false, reason: 'System error' });
    }
};

let getActiveAlerts = async (req, res) => {
    try {
        const response = await axios.get(`${orionUrl}?type=Alert`, {
            headers: getHeaders,
            params: {
                q: 'status==active'
            }
        });
        res.json({ data: response.data });
    } catch (error) {
        console.error('Alerts error in getActiveAlerts:', error);
        res.status(500).json({ error: 'Failed to fetch active alerts' });
    }
}

let getAlertLocation = async (req, res) => {
    const alertId = req.params.id;
    
    try {
        const response = await axios.get(`${orionUrl}/${alertId}`, {
            headers: getHeaders,
            params: {
                attrs: 'location'
            }
        });

        if (!response.data.location?.value?.coordinates) {
            return res.status(404).json({ error: 'Coordinates not found' });
        }

        const coordinates = response.data.location.value.coordinates[0]
            .map(([lng, lat]) => [lat, lng ]);

        res.json(coordinates);
    } catch (error) {
        console.error('Alert location error in getAlertLocation:', error);
        res.status(500).json({ error: 'Failed to fetch alert location' });
    }
}

let patchAlertStatus = async (req, res) => {
    const alertId = req.params.id;
    const { status } = req.body;

    try {
        const response = await axios.patch(`${orionUrl}/${alertId}/attrs`, {
            status: {
                type: 'Text',
                value: status
            }
        }, {
            headers: patchHeaders
        });

        res.json({ 
            message: 'Status updated successfully',
            data: response.data 
        });
    } catch (error) {
        console.error('Alert patch error:', error);
        const statusCode = error.response?.status || 500;
        res.status(statusCode).json({ 
            error: error.response?.data?.error || 'Failed to update alert status' 
        });
    }
};

let patchAlertLocation = async (req, res) => {
    const alertId = req.params.id;
    const { location } = req.body;
    
    const payload = {
        "location": {
            "type": "geo:json",
            "value": {
                "type": "Point",
                "coordinates": [location.lng, location.lat]
            }
        }
    };

    try {
        const response = await axios.patch(`${orionUrl}/${alertId}/attrs`, payload, {
            headers: patchHeaders
        });

        res.json({ 
            message: 'Location updated successfully',
            data: response.data 
        });
    } catch (error) {
        console.error('Alert patch error in patchAlertLocation:', error);
        const statusCode = error.response?.status || 500;
        res.status(statusCode).json({ 
            error: error.response?.data?.error || 'Failed to update alert location' 
        });
    }
}

let patchAlertActionTaken = async (req, res) => {
    const alertId = req.params.id;
    const { action } = req.body;

    try {
        const response = await axios.patch(`${orionUrl}/${alertId}/attrs`, {
            actionTaken: {
                type: 'Text',
                value: action
            }
        }, {
            headers: patchHeaders
        });

        res.json({ 
            message: 'Action taken updated successfully',
            data: response.data 
        });
    } catch (error) {
        console.error('Alert patch error in patchAlertActionTaken:', error);
        const statusCode = error.response?.status || 500;
        res.status(statusCode).json({ 
            error: error.response?.data?.error || 'Failed to update alert action' 
        });
    }
};

let getAllSmartLocks = async (req, res) => {
    try {
        // Type is Device and name starts with SmartLock-
        // const response = await axios.get(`${orionUrl}?type=Device&limit=1000&q=name~=^SmartLock-`, {
        //     headers: getHeaders
        // });
        const response = await axios.get(`${orionUrl}`, {
            headers: getHeaders,
            params: {
                type: 'Device',
                limit: 1000,
                q: 'name~=^SmartLock-'
            }
        });
        res.json({ data: response.data });
    } catch (error) {
        console.error('Smart locks error in getAllSmartLocks:', error);
        res.status(500).json({ error: 'Failed to fetch smart locks' });
    }
};

let fetchCameraImage = async (req, res) => {
    try {
        cameraController.getLatestImage(req, res);
    } catch (error) {
        console.error('Error fetching camera image:', error);
        res.status(500).json({ error: 'Failed to fetch camera image' });
    }
};

import * as trackingDataController from './trackingDataController.mjs';
let handleTrackingData = async (req, res) => {
    try {
        const trackingData = req.body;
        
        // write tracking data to the database
        await trackingDataController.writeWorkerTrackingData(trackingData);

        res.json({ message: 'Tracking data received' });
    } catch (error) {
        console.error('Tracking data error in handleTrackingData:', error);
        res.status(500).json({ error: 'Failed to handle tracking data' });
    }
};

let getHistoricTrackingData = async (req, res) => {
    // expects query ?date=YYYY-MM-DD&person_id=person_id
    try {
        const date = req.query.date;
        const personId = req.query.person_id;
        const trackingData = await trackingDataController.fetchHistoricTrackingData(date, personId);
        res.json(trackingData);
    } catch (error) {
        console.error('Historic tracking data error:', error);
        res.status(500).json({ error: 'Failed to fetch historic tracking data' });
    }
}


// let getSmartLockData = async(req, res) => {
//     try {
//         const smartLockId = req.params.id;
//         const response = await axios.get(`${orionUrl}/${smartLockId}`, {
//             headers: getHeaders
//         });
//         res.json({ data: response.data });
//     } catch (error) {
//         console.error('Smart lock error:', error);
//         res.status(500).json({ error: 'Failed to fetch smart lock data' });
//     }
// }



export { getData, getAllData, getDeviceData, getDeviceDataFromName, getDeviceLocationData, 
    getAllDevicesLocationData, getAllDevicesControlledAssets, saveCoordinates, getAllFacilities, 
    getFacilityLocationData, getFacilitiesNameAndLocation, findCurrentFacilities, getDoorsLocations, 
    getPersonData, getAllPeopleData, handleSOSAlert, handleMaintenanceSchedule, getScheduledMaintenances,
    updateMaintenanceStatus, checkAccessAuthorization, getActiveAlerts, getAlertLocation, patchAlertStatus, patchAlertLocation, 
    patchAlertActionTaken, getAllSmartLocks, fetchCameraImage, handleTrackingData, getHistoricTrackingData, 
    // getSmartLockData,
 };
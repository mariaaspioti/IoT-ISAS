import * as APICall from './api';

export const fetchTrackingData = async () => {
    try {
        // Fetch all devices' locations
        const data = await APICall.fetchAllDevicesLocations();
        console.log('Device data:', data);


        // Fetch all devices' controlledAssets i.e. people being tracked
        const controlledAssets = await APICall.fetchAllDevicesControlledAssets();
        console.log('Controlled assets data:', controlledAssets);
        // setPeople(controlledAssets);

        // const controlledAssetsMap = controlledAssets.reduce((acc, person) => ({
        //     ...acc,
        //     [person.device_id]: person
        //   }), {});
        // console.log("controlledAssetsMap:", controlledAssetsMap);


        // Determine the Facility in which the device is located
        const facilities = await APICall.findCurrentFacilities(data);
        // console.log('Facilities data:', facilities);

        // 1. Map each device to its facility
        const deviceFacilityMap = data.reduce((acc, device, index) => {
            acc[device.id] = facilities[index];
            return acc;
        }, {});

        // console.log("deviceFacilityMap:", JSON.stringify(deviceFacilityMap, null, 2));
        // console.log("deviceFacilityMap:", deviceFacilityMap);

        // 2. Map each person to their BT and GPS devices
        const personDevicesMap = data.reduce((acc, device) => {
            const personIds = device.controlledAsset || [];
            const isBT = device.name.startsWith('BluetoothTracker');
            personIds.forEach(personId => {
                if (!acc[personId]) acc[personId] = { bt: null, gps: null };
                isBT ? (acc[personId].bt = device) : (acc[personId].gps = device);
            });
            return acc;
        }, {});

        // console.log("personDevicesMap:", JSON.stringify(personDevicesMap, null, 2));
        // console.log("personDevicesMap:", personDevicesMap);

        // 3. Build mapData based on people and their indoor/outdoor status
        let mapData = controlledAssets.map(person => {
            console.log("person:", person);
            const devices = personDevicesMap[person.person_id]|| {};
            console.log("devices:", devices);
            const isIndoors = person.isIndoors;
            const selectedDevice = isIndoors ? devices.bt : devices.gps;
            console.log("selectedDevice:", selectedDevice);
            
            if (!selectedDevice) {
                console.warn(`No device found for person ${person.person_id}`);
                // return { lat: 53.373289, lng: -6.521759, message: 'No device found' };
                return null;
            }

            const facility = deviceFacilityMap[selectedDevice.id];
            const lng = selectedDevice.lng;
            const lat = selectedDevice.lat;
            const initials = person.person_name.split(' ').map(n => n[0]).join('');
            // console.log("selectedDevice:", selectedDevice);
            const selectedDeviceNum = selectedDevice.id.split('Device:')[1];

            return {
                lat,
                lng,
                facility_name: facility?.name || 'Outside',
                facility_id: facility?.id || 'Outside',
                ...person,
                tracking_type: isIndoors ? 'Bluetooth' : 'GPS',
                message: `Device: ${selectedDeviceNum} | Facility: ${facility?.name || 'Outside'}, Person: ${initials}`
            };
        }).filter(Boolean);
        // DEBUG: accept first the persons with urn:ngsi-ld:Person:0, 1, 2
        mapData = mapData.filter(person => person.person_id === 'urn:ngsi-ld:Person:0' || person.person_id === 'urn:ngsi-ld:Person:1'
            || person.person_id === 'urn:ngsi-ld:Person:2' || person.person_id === 'urn:ngsi-ld:Person:3'
            || person.person_id === 'urn:ngsi-ld:Person:4' || person.person_id === 'urn:ngsi-ld:Person:5'
            || person.person_id === 'urn:ngsi-ld:Person:6' || person.person_id === 'urn:ngsi-ld:Person:7'
            || person.person_id === 'urn:ngsi-ld:Person:8' || person.person_id === 'urn:ngsi-ld:Person:9' 
        );
        
        return { mapData, facilities, controlledAssets, data };
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }
};

export const showDoors = async () => {
    const data = await APICall.fetchDoorsLocations();
    // console.log('Door data:', data);
    // form: { id: 'Door1', location: { type: 'geo:json', value: {type: 'Point', coordinates: [ 51.5074, 0.1278 ] } } }

    const mapData = data.map((door, index) => {
        return {
            lat: door.location.value.coordinates[1],
            lng: door.location.value.coordinates[0],
            message: `Door: ${door.id}`
        };
    });

    return mapData;
}

export const showBuildings = async () => {
    const data = await APICall.fetchBuildingsLocations();
    // console.log('Building data in showBuildings:', data);
    // form: { id: 'Building1', location: { type: 'geo:json', value: {type: 'Polygon', coordinates: [ [ [ 51.5074, 0.1278 ], [ 51.5074, 0.1278 ], [ 51.5074, 0.1278 ] ] } } }

    const mapData = data.flatMap((building) => {
        const coordinates = building.location.value.coordinates[0];
        return coordinates.map(coord => ({
            lat: coord[1],
            lng: coord[0],
            name: building.name.value,
            message: `Building: ${building.id}`
        }));
    });

    return mapData;
}

export const fetchFormatAlertData = async (alertData) => {
    // // Given an alert, fetch the device data that caused it with known name
    const deviceName = alertData.alertSource.value[0];
    // console.log("Device Name:", deviceName, "in fetchFormatAlertData");
    const arr = await APICall.fetchDeviceDataGivenName(deviceName);
    const deviceData = arr[0];
    // console.log("Device Data:", deviceData, "in fetchFormatAlertData");
    // Extract the controlled asset (person id) from the device data
    const personId = deviceData.controlledAsset.value;
    // Fetch the person data
    const personData = await APICall.fetchPersonData(personId);
    
    // given the person data, recover their devices with 'hasDevices' relationship
    console.log("personData:", personData, "in fetchFormatAlertData");
    // console.log("personData.hasDevices:", personData.hasDevices, "in fetchFormatAlertData");
    const deviceIds = personData.hasDevices.value;
    console.log("deviceIds:", deviceIds, "in fetchFormatAlertData");
    // Fetch the device data
    // console.log("deviceIds:", deviceIds);
    const devicesData = await Promise.all(deviceIds.map(deviceId => APICall.fetchDeviceData(deviceId)));
    console.log("devicesData:", devicesData);

    // If the person is indoors, keep the location indicated by the device with name starting with 'BluetoothTracker'
    // Otherwise, keep the location indicated by the device with name starting with 'GPS'
    let deviceLocation;
    if (personData.isIndoors.value) {
        deviceLocation = devicesData.find(device => 
            device.name.value.startsWith('BluetoothTracker')).location.value.coordinates;
    } else {
        deviceLocation = devicesData.find(device => 
            device.name.value.startsWith('GPS')).location.value.coordinates;
    }
    console.log("deviceLocation:", deviceLocation, "in fetchFormatAlertData");
    // Find the facility in which the device is located
    const locationData = { lat: deviceLocation[1], lng: deviceLocation[0] };
    const facilities = await APICall.findCurrentFacilities([locationData]);
    const facility = facilities[0];
    console.log("facility:", facility, "in fetchFormatAlertData");

    // Format the alert data
    const formattedData = {
        id: alertData.id,
        description: alertData.description.value,
        severity: alertData.severity.value,
        status: alertData.status.value,
        frontend_timestamp: new Date().toLocaleString(),
        personName: personData.name.value,
        personId: personData.id,
        // personIsIndoors: personData.isIndoors.value,
        personCurrentLocation: deviceLocation,
        personCurrentFacility: facility.name
    };

    console.log('Formatted alert data:', formattedData);
    return formattedData;
    // return alertData;
}
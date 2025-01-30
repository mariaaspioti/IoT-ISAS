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

        const controlledAssetsMap = controlledAssets.reduce((acc, person) => ({
            ...acc,
            [person.device_id]: person
          }), {});
        console.log("controlledAssetsMap:", controlledAssetsMap);


        // Determine the Facility in which the device is located
        const facilities = await APICall.findCurrentFacilities(data);
        console.log('Facilities data:', facilities);

        // 1. Map each device to its facility
        const deviceFacilityMap = data.reduce((acc, device, index) => {
            acc[device.id] = facilities[index];
            return acc;
        }, {});

        // console.log("deviceFacilityMap:", JSON.stringify(deviceFacilityMap, null, 2));
        console.log("deviceFacilityMap:", deviceFacilityMap);

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
        console.log("personDevicesMap:", personDevicesMap);

        // 3. Build mapData based on people and their indoor/outdoor status
        let mapData = controlledAssets.map(person => {
            console.log("person:", person);
            const devices = personDevicesMap[person.person_id]|| {};
            // console.log("devices:", devices);
            const isIndoors = person.isIndoors;
            const selectedDevice = isIndoors ? devices.bt : devices.gps;
            // console.log("selectedDevice:", selectedDevice);
            
            if (!selectedDevice) {
                console.warn(`No device found for person ${person.person_id}`);
                // return { lat: 53.373289, lng: -6.521759, message: 'No device found' };
                return null;
            }

            const facility = deviceFacilityMap[selectedDevice.id];
            const lng = selectedDevice.lng;
            const lat = selectedDevice.lat;
            const initials = person.person_name.split(' ').map(n => n[0]).join('');
            console.log("selectedDevice:", selectedDevice);
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
        // DEBUG: accept first the persons with urn:ngsi-ld:Person:0 and urn:ngsi-ld:Person:1
        mapData = mapData.filter(person => person.person_id === 'urn:ngsi-ld:Person:0' || person.person_id === 'urn:ngsi-ld:Person:1');

        // console.log("mapData:", JSON.stringify(mapData, null, 2));
        console.log("mapData:", mapData);

        // // Set the map data
        // const mapData = data.map((loc, index) => {
        //     const person = controlledAssetsMap[loc.id];
        //     const facility = facilities[index]; // Ensure order preservation!
        //     const personInitials = person?.person_name?.split(' ').map(name => name[0]).join('') || 'N/A';
        //     const device_num = loc.id.split('Device:')[1];
        //     return {
        //       lat: loc.lat,
        //       lng: loc.lng,
        //       facility_name: facility?.name || 'Unknown',
        //       facility_id: facility?.id || 'Unknown',
        //       ...(person || {}),
        //       message: `Device: ${device_num} | Facility: ${facility?.name}, Person: ${personInitials || 'None'}`
        //     };
        // });
        // console.log("mapData:", mapData);
        
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
    console.log('Building data:', data);
    // form: { id: 'Building1', location: { type: 'geo:json', value: {type: 'Polygon', coordinates: [ [ [ 51.5074, 0.1278 ], [ 51.5074, 0.1278 ], [ 51.5074, 0.1278 ] ] } } }

    const mapData = data.flatMap((building) => {
        const coordinates = building.location.value.coordinates[0];
        return coordinates.map(coord => ({
            lat: coord[1],
            lng: coord[0],
            message: `Building: ${building.id}`
        }));
    });

    return mapData;
}
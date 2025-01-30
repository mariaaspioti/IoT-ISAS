import * as APICall from './api';

export const fetchTrackingData = async () => {
    try {
        // Fetch all devices' locations
        const data = await APICall.fetchAllDevicesLocations();
        console.log('Device data:', data);
        // setCoordinates(data);
        // setLoading(false);

        // Fetch all devices' controlledAssets i.e. people being tracked
        const controlledAssets = await APICall.fetchAllDevicesControlledAssets();
        console.log('Controlled assets data:', controlledAssets);
        // setPeople(controlledAssets);

        const controlledAssetsMap = controlledAssets.reduce((acc, person) => ({
            ...acc,
            [person.device_id]: person
          }), {});


        // Determine the Facility in which the device is located
        const facilities = await APICall.findCurrentFacilities(data);
        console.log('Facilities data:', facilities);
        // setCurrentLocations(facilities);

        // Set the map data
        const mapData = data.map((loc, index) => {
            const person = controlledAssetsMap[loc.id];
            const facility = facilities[index]; // Ensure order preservation!
            const personInitials = person?.person_name?.split(' ').map(name => name[0]).join('') || 'N/A';
            return {
              lat: loc.lat,
              lng: loc.lng,
              facility_name: facility?.name || 'Unknown',
              facility_id: facility?.id || 'Unknown',
              ...(person || {}),
              message: `Device: ${loc.id.slice(-1)}, Facility: ${facility?.name}, Person: ${personInitials || 'None'}`
            };
        });
        console.log("mapData:", mapData);
        
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
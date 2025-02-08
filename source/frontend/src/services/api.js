// Fetch 
export const fetchLocations = async () => {
    try {
        const response = await fetch('/api/data');
        const json = await response.json();
        return json.data;
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }
};

// Fetch all data
export const fetchAllLocations = async () => {
    try {
        const response = await fetch('/api/all-data');
        const json = await response.json();
        return json.data;
    } catch (error) {
        console.error('Error fetching all data:', error);
        throw error;
    }
};

// Fetch device data
export const fetchDeviceData = async (device_id) => {
    try {
        const response = await fetch(`/api/devices/${device_id}`);
        const json = await response.json();
        return json.data;
    } catch (error) {
        console.error('Error fetching device data in fetchDeviceData:', error);
        throw error;
    }
};

// Fetch device data given a name
export const fetchDeviceDataGivenName = async (device_name) => {
    try {
        const response = await fetch(`/api/devices/name/${device_name}`);
        const json = await response.json();
        return json.data;
    } catch (error) {
        console.error('Error fetching device data in fetchDeviceDataGivenName:', error);
        throw error;
    }
};

// Fetch device location data
export const fetchDeviceLocation = async (device_id) => {
    try {
        const response = await fetch(`/api/devices/${device_id}`);
        const json = await response.json();
        return json.data;
    } catch (error) {
        console.error('Error fetching device data in fetchDeviceLocation:', error);
        throw error;
    }
};

// Fetch all devices' location data
export const fetchAllDevicesLocations = async () => {
    try {
        const response = await fetch('/api/devices/location');
        const json = await response.json();
        return json.data;
    } catch (error) {
        console.error('Error fetching devices data:', error);
        throw error;
    }
};

// Fetch all devices' controlledAssets data
export const fetchAllDevicesControlledAssets = async (devices) => {
    try {
        const response = await fetch('/api/devices/controlledAssets');
        const json = await response.json();
        return json.data;
    } catch (error) {
        console.error('Error fetching controlledAssets data:', error);
        throw error;
    }
}

// Save coordinates
export const saveCoordinates = async (coordinate) => {
    try {
        const response = await fetch('/api/save-coordinates', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(coordinate),
        });
        if (!response.ok) {
            throw new Error('Failed to save coordinates');
        }
        console.log('Coordinate saved successfully');
    } catch (error) {
        console.error('Error saving coordinate:', error);
    }
};


// Find the current facilities in which the person (coordinates) is located
export const findCurrentFacilities = async (coordinates) => {
    try {
        // Send coordinates to the server for calculation
        const response = await fetch('/api/facilities/find', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ coordinates })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const json = await response.json();
        return json.data; // Expect the server to return enriched coordinates
    } catch (error) {
        console.error('Error fetching facilities data:', error);
        throw error;
    }
};

// Fetch facilities-buildings data
export const fetchAllBuildingsData = async () => {
    try {
        const response = await fetch('/api/facilities');
        const json = await response.json();
        return json.data;
    } catch (error) {
        console.error('Error fetching facilities data:', error);
        throw error;
    }
}

// Fetch facilities-buildings coordinates
export const fetchBuildingsLocations = async () => {
    try {
        const response = await fetch('/api/facilities/name-location');
        const json = await response.json();
        return json.data;
    } catch (error) {
        console.error('Error fetching facilities data:', error);
        throw error;
    }
};


// Fetch doors locations
export const fetchDoorsLocations = async () => {
    try {
        const response = await fetch('/api/doors/location');
        const json = await response.json();
        return json.data;
    } catch (error) {
        console.error('Error fetching doors data:', error);
        throw error;
    }
};

// Fetch all people data
export const fetchAllPeopleData = async () => {
    try {
        const response = await fetch('/api/people');
        const json = await response.json();
        return json.data;
    } catch (error) {
        console.error('Error fetching people data:', error);
        throw error;
    }
};

// Fetch person data
export const fetchPersonData = async (person_id) => {
    try {
        const response = await fetch(`/api/people/${person_id}`);
        const json = await response.json();
        return json.data;
    } catch (error) {
        console.error('Error fetching person data:', error);
        throw error;
    }
};

// Post Maintenance Schedule
export const postMaintenanceSchedule = async (schedule) => {
    try {
        const response = await fetch('/api/maintenance', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(schedule)
        });
        
        if (!response.ok) throw new Error('Scheduling failed');
        
        const newSchedule = await response.json();
        return newSchedule;
    } catch (error) {
        console.error('Scheduling error:', error);
        throw error;
    }
};

// Fetch Access Authorization
export const fetchAccessAuthorization = async (personId, buildingId) => {
    try {
        const response = await fetch(`/api/access-check?person=${personId}&building=${buildingId}`);
        const { authorized, reason } = await response.json();
        return { authorized, reason };
    } catch (error) {
        console.error('Error fetching access authorization data:', error);
        throw error;
    }
};
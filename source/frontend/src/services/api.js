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
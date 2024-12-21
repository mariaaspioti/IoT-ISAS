export const fetchLocations = async () => {
    try {
        const response = await fetch('/api/data');
        const json = await response.json();
        return json.data; // Assuming data contains an array of coordinates
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }
};

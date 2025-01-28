import React, { useState, useEffect } from 'react';
import './App.css';
import Map from './components/Map';
import * as APICall from './services/api';

function App() {
    const [coordinates, setCoordinates] = useState([]);
    const [loading, setLoading] = useState(true);
    const [currentLocations, setCurrentLocations] = useState([]);
    const [mapData, setMapData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await APICall.fetchAllDevicesLocations();
                console.log('Device data:', data);
                setCoordinates(data);
                setLoading(false);
        
                // Determine the Facility in which the device is located
                const facilities = await APICall.findCurrentFacilities(data);
                console.log('Facilities data:', facilities);
                setCurrentLocations(facilities);

                // Set the map data
                const coordinatesAndCurrentLocations = data.map((loc, index) => {
                    const facility = facilities[index];
                    return {
                        ...loc,
                        facility: facility?.name || 'Unknown',
                        facility_id: facility?.id || 'Unknown',
                    };
                });
                console.log("Coordinates and current locations:", coordinatesAndCurrentLocations);
                setMapData(coordinatesAndCurrentLocations);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData(); // Initial fetch
        const interval = setInterval(fetchData, 2000); // Fetch every 2 seconds

        return () => clearInterval(interval); // Cleanup on unmount
    }, []);

    return (
        <div>
            <h1>React + Node.js</h1>
            <h3>Updates every 5 seconds, with data retrieved from the Node server.</h3>
            <p>Click on the markers to see their coordinates and message/id.</p>
            {loading ? <p>Loading...</p> : <Map data = {mapData} />}
        </div>
    );
}

export default App;

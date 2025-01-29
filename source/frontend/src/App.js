import React, { useState, useEffect } from 'react';
import './App.css';
import Map from './components/Map';
import * as APICall from './services/api';

function App() {
    const [coordinates, setCoordinates] = useState([]);
    const [loading, setLoading] = useState(true);
    const [currentLocations, setCurrentLocations] = useState([]);
    const [people, setPeople] = useState([]);
    const [mapData, setMapData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                // Fetch all devices' locations
                const data = await APICall.fetchAllDevicesLocations();
                console.log('Device data:', data);
                setCoordinates(data);
                setLoading(false);

                // Fetch all devices' controlledAssets i.e. people being tracked
                const controlledAssets = await APICall.fetchAllDevicesControlledAssets();
                console.log('Controlled assets data:', controlledAssets);
                setPeople(controlledAssets);

                const controlledAssetsMap = controlledAssets.reduce((acc, person) => ({
                    ...acc,
                    [person.device_id]: person
                  }), {});

        
                // Determine the Facility in which the device is located
                const facilities = await APICall.findCurrentFacilities(data);
                console.log('Facilities data:', facilities);
                setCurrentLocations(facilities);

                // Set the map data
                const mapData = data.map((loc, index) => {
                    const person = controlledAssetsMap[loc.id];
                    const facility = facilities[index]; // Ensure order preservation!
                  
                    return {
                      lat: loc.lat,
                      lng: loc.lng,
                      facility_name: facility?.name || 'Unknown',
                      facility_id: facility?.id || 'Unknown',
                      ...(person || {}),
                      message: `Device: ${loc.id}, Facility: ${facility?.name}, Person: ${person?.person_name || 'None'}`
                    };
                });
                console.log("mapData:", mapData);
                setMapData(mapData);
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

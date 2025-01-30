import React, { useState, useEffect } from 'react';
import './App.css';
import Map from './components/Map';
// import * as APICall from './services/api';
import * as editMap from './services/editMap';

function App() {
    // const [coordinates, setCoordinates] = useState([]);
    const [loading, setLoading] = useState(true);
    // const [currentLocations, setCurrentLocations] = useState([]);
    // const [people, setPeople] = useState([]);
    const [mapData, setMapData] = useState([]);

    const fetchData = async () => {
        try {
            const { mapData, facilities, controlledAssets, data } = await editMap.fetchTrackingData();
            // console.log("Data:", mapData, facilities, controlledAssets, data);
            
            setMapData(mapData);
            // setCurrentLocations(facilities);
            // setPeople(controlledAssets);
            // setCoordinates(data);
            setLoading(false);

            // ==== Debugging ====
            // const mapData1 = await editMap.showDoors();
            // const mapData2 = await editMap.showBuildings();

            //combine the two objects
            // const mapData = [ ...mapData1, ...mapData2 ];

            // console.log("components", mapData1, mapData2);
            // setMapData(mapData);
        } catch (error) {
            console.error('Error fetching data:', error);
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();

        const interval = setInterval(fetchData, 2000); // Fetch every 2 seconds
        setLoading(false);

        return () => clearInterval(interval); // Cleanup on unmount
    }, []);

    if (loading) {
        return <p>Loading...</p>;
    }

    return (
        <div>
            <h1>React + Node.js</h1>
            <h3>Updates every 2 seconds, with data retrieved from the Node server.</h3>
            <p>Click on the markers to see their coordinates and message/id.</p>
            {loading ? <p>Loading...</p> : <Map data = {mapData} />}
        </div>
    );
}

export default App;

import React, { useState, useEffect } from 'react';
import './App.css';
import Map from './components/Map';
import { fetchLocations } from './services/api';

function App() {
    const [locations, setLocations] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = () => {
            fetchLocations()
                .then((data) => {
                    setLocations(data);
                    setLoading(false);
                })
                .catch((error) => console.error('Error fetching data:', error));
        };

        fetchData(); // Initial fetch
        const interval = setInterval(fetchData, 5000); // Fetch every 5 seconds

        return () => clearInterval(interval); // Cleanup on unmount
    }, []);

    return (
        <div>
            <h1>React + Node.js</h1>
            <h3>Updates every 5 seconds, with data retrieved from the Node server.</h3>
            <p>Click on the markers to see their coordinates and message/id.</p>
            {loading ? <p>Loading...</p> : <Map locations={locations} />}
        </div>
    );
}

export default App;

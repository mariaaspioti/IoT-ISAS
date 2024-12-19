import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import L from 'leaflet';
import './App.css';
import 'leaflet/dist/leaflet.css';

// Import marker icon images
import iconRetinaUrl from 'leaflet/dist/images/marker-icon-2x.png';
import iconUrl from 'leaflet/dist/images/marker-icon.png';
import shadowUrl from 'leaflet/dist/images/marker-shadow.png';

// Fix for default marker icon paths
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl,
  iconUrl,
  shadowUrl,
});

function App() {
    const [locations, setLocations] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
      const fetchData = () => {
          fetch('/api/data')
              .then((response) => response.json())
              .then((json) => {
                  setLocations(json.data); // Assuming data contains an array of coordinates
                  setLoading(false);
              })
              .catch((error) => console.error('Error fetching data:', error));
      };

      fetchData(); // Initial fetch
      const interval = setInterval(fetchData, 5000); // Fetch every 5 seconds

      return () => clearInterval(interval); // Cleanup on component unmount
    }, []);

    return (
        <div>
            <h1>React + Node.js</h1>
            <h3> Updates every 5 seconds, with data retrieved from the Node server.</h3>
            <p> Click on the markers to see their coordinates and message/id.</p>
            {loading ? (
                <p>Loading...</p>
            ) : (
                <MapContainer center={[51.505, -0.09]} zoom={13} className="leaflet-container">
                    <TileLayer
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                        attribution="&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors"
                    />
                    {locations.map((loc, index) => (
                        <CircleMarker
                            key={index}
                            center={[loc.lat, loc.lng]}
                            radius={8} // Size of the dot
                            color="blue" // Border color
                            fillColor="blue" // Fill color
                            fillOpacity={0.6} // Transparency
                        >
                            <Popup>
                                <strong>Coordinates:</strong> {loc.lat}, {loc.lng}
                                <strong> Message:</strong> {loc.msg? loc.msg : 'No message'}
                            </Popup>
                        </CircleMarker>
                    ))}
                </MapContainer>
            )}
        </div>
    );
}

export default App;

// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <div className="App">
//           <h1>This is my first React App!</h1>
//           <p>This is my first React Component, yay!</p>
//         </div>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;

import React from 'react';
import { MapContainer, TileLayer, useMapEvent } from 'react-leaflet';
import CircleMarkerPopup from './CircleMarkerPopup';
import 'leaflet/dist/leaflet.css';
import { saveCoordinates } from '../services/api';

const ClickLogger = () => {
    useMapEvent('click', (e) => {
        const { lat, lng } = e.latlng;
        console.log(`Clicked at latitude: ${lat}, longitude: ${lng}`);
        saveCoordinates({ lat, lng }); // Send to backend
    });
    return null;
};

// "lat": 53.37575635880662,
// "lng": -6.5230679512023935

const Map = ({ locations }) => {
    return (
        <MapContainer center={[53.37575635880662, -6.5230679512023935]} zoom={13} className="leaflet-container">
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution="&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors"
            />
            <ClickLogger /> {/* Add click listener */}
            {locations.map((loc, index) => (
                <CircleMarkerPopup key={index} location={loc} />
            ))}
        </MapContainer>
    );
};

export default Map;

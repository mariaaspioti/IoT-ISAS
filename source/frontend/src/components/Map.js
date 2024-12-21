import React from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import CircleMarkerPopup from './CircleMarkerPopup';
import 'leaflet/dist/leaflet.css';

const Map = ({ locations }) => {
    return (
        <MapContainer center={[51.505, -0.09]} zoom={13} className="leaflet-container">
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution="&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors"
            />
            {locations.map((loc, index) => (
                <CircleMarkerPopup key={index} location={loc} />
            ))}
        </MapContainer>
    );
};

export default Map;

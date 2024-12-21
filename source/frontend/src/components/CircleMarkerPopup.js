import React from 'react';
import { CircleMarker, Popup } from 'react-leaflet';

const CircleMarkerPopup = ({ location }) => {
    return (
        <CircleMarker
            center={[location.lat, location.lng]}
            radius={8} // Size of the dot
            color="blue" // Border color
            fillColor="blue" // Fill color
            fillOpacity={0.6} // Transparency
        >
            <Popup>
                <strong>Coordinates:</strong> {location.lat}, {location.lng}
                <br />
                <strong>Message:</strong> {location.msg || 'No message'}
            </Popup>
        </CircleMarker>
    );
};

export default CircleMarkerPopup;

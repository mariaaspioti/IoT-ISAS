import React from 'react';
import { CircleMarker, Popup } from 'react-leaflet';

const CircleMarkerPopup = ({ data }) => {
    return (
        <CircleMarker
            center={[data.lat, data.lng]}
            radius={8} // Size of the dot
            color="blue" // Border color
            fillColor="blue" // Fill color
            fillOpacity={0.6} // Transparency
        >
            <Popup>
                <strong>Coordinates:</strong> {data.lat}, {data.lng}
                <br />
                <strong>Current Facility:</strong> {data.facility}
                <br />
                <strong>Message:</strong> {data.msg || 'No message'}
            </Popup>
        </CircleMarker>
    );
};

export default CircleMarkerPopup;

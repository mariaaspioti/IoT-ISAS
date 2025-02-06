import React from 'react';
import { CircleMarker, Popup } from 'react-leaflet';

const CircleMarkerPopup = ({ type, data, color, fillColor, radius, fillOpacity }) => {
    // Common properties for all CircleMarkers
    const commonProps = {
      center: [data.lat, data.lng],
      color,
      fillColor,
      radius,
      fillOpacity,
    };
  
    // Determine popup content based on type
    let popupContent;
    if (type === 'door') {
      popupContent = <strong>{data.message}</strong>;
    } else if (type === 'person') {
      popupContent = (
        <>
          <strong>Coordinates:</strong> {data.lat}, {data.lng}<br />
          <strong>Belongs To:</strong> {data.person_name}<br />
          <strong>Current Facility:</strong> {data.facility_name}<br />
          <strong>Tracking Method:</strong> {data.tracking_type}<br />
          <strong>Message:</strong> {data.message || 'No message'}
        </>
      );
    } else {
      // Generic popup content for any other type
      popupContent = (
        <>
          <strong>Coordinates:</strong> {data.lat}, {data.lng}<br />
          <strong>Message:</strong> {data.message || 'No message'}
        </>
      );
    }
  
    return (
      <CircleMarker {...commonProps}>
        <Popup>
          {popupContent}
        </Popup>
      </CircleMarker>
    );
  };

export default CircleMarkerPopup;

import React, { useRef, useEffect, useState } from 'react';
import { CircleMarker, Popup } from 'react-leaflet';

const CircleMarkerPopup = ({ type, data, color, fillColor, radius, fillOpacity }) => {
  const markerRef = useRef(null);
  const [popupOpen, setPopupOpen] = useState(false);

  // Set up event listeners to track popup open/close
  useEffect(() => {
    if (markerRef.current) {
      const marker = markerRef.current;
      const onPopupOpen = () => setPopupOpen(true);
      const onPopupClose = () => setPopupOpen(false);

      marker.on('popupopen', onPopupOpen);
      marker.on('popupclose', onPopupClose);

      // Cleanup when component unmounts
      return () => {
        marker.off('popupopen', onPopupOpen);
        marker.off('popupclose', onPopupClose);
      };
    }
  }, []);

  // When data changes, update the marker position in place.
  useEffect(() => {
    if (markerRef.current) {
      markerRef.current.setLatLng([data.lat, data.lng]);
      // If the popup was open, re-open it after updating the position.
      if (popupOpen) {
        markerRef.current.openPopup();
      }
    }
  }, [data.lat, data.lng, popupOpen]);

  let popupContent;
  if (type === 'door') {
    popupContent = <strong>{data.message}</strong>;
  } else if (type === 'person') {
    popupContent = (
      <>
        <strong>Coordinates:</strong> {data.lat}, {data.lng}
        <br />
        <strong>Belongs To:</strong> {data.person_name}
        <br />
        <strong>Current Facility:</strong> {data.facility_name}
        <br />
        <strong>Tracking Method:</strong> {data.tracking_type}
        <br />
        <strong>Message:</strong> {data.message || 'No message'}
      </>
    );
  } else {
    popupContent = (
      <>
        <strong>Coordinates:</strong> {data.lat}, {data.lng}
        <br />
        <strong>Message:</strong> {data.message || 'No message'}
      </>
    );
  }

  return (
    <CircleMarker
      ref={markerRef}
      center={[data.lat, data.lng]}
      color={color}
      fillColor={fillColor}
      radius={radius}
      fillOpacity={fillOpacity}
    >
      <Popup>{popupContent}</Popup>
    </CircleMarker>
  );
};

export default CircleMarkerPopup;
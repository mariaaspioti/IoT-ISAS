import React, { useMemo } from 'react';
import { MapContainer, TileLayer, useMapEvent, Polygon, Popup } from 'react-leaflet';
import CircleMarkerPopup from './CircleMarkerPopup';
import 'leaflet/dist/leaflet.css';
import { saveCoordinates } from '../../services/api';

const ClickLogger = () => {
  useMapEvent('click', (e) => {
    const { lat, lng } = e.latlng;
    console.log(`Clicked at latitude: ${lat}, longitude: ${lng}`);
    saveCoordinates({ lat, lng }); // Send to backend
  });
  return null;
};

const MARKER_COLORS = {
  buildings: 'darkred',
  doors: 'green',
  people: 'blue',
  alert: 'red',
};

const Map = ({ data, viewType, alerts }) => {
  // Use memoization for markers or polygons to optimize rendering.
  const renderedElements = useMemo(() => {
    if (viewType === 'buildings') {
      // Group building data by building id extracted from the message.
      const buildingGroups = {};
      data.forEach((item) => {
        // Assuming messages are of the form: "Building: urn:ngsi-ld:Building:<id>"
        const parts = item.message.split(':');
        const buildingId = parts[parts.length - 1].trim();
        if (!buildingGroups[buildingId]) {
          buildingGroups[buildingId] = [];
        }
        // Each building group gets an array of coordinate pairs and name.
        buildingGroups[buildingId].push([item.lng, item.lat, item.name]);
      });

      // Create a polygon for each building group.
      return Object.entries(buildingGroups).map(([buildingId, positions]) => {
        const name = positions[0][2];
        const coordinates = positions.map(([lng, lat]) => [lat, lng]);
        return <Polygon key={buildingId} positions={coordinates} color={MARKER_COLORS[viewType] || 'red'}>
          <Popup>
            <strong>Building:</strong> {name}
          </Popup>
        </Polygon>
        });
    } else if (viewType === 'doors') {
      // For doors or people, render individual markers.
      return data.map((mdata) => (
        <CircleMarkerPopup
          key={mdata.message.split('Door: ')[1]}
          type={'door'}
          data={mdata}
          color={MARKER_COLORS[viewType] || 'green'}
          fillColor={MARKER_COLORS[viewType] || 'green'}
          radius={5}
          fillOpacity={1}
        />
      ));
    } else if (viewType === 'people') {
      // For doors or people, render individual markers.
      return data.map((mdata) => (
        <CircleMarkerPopup
          key={mdata.person_id}
          type={'person'}
          data={mdata}
          color={MARKER_COLORS[viewType] || 'blue'}
          fillColor={MARKER_COLORS[viewType] || 'blue'}
          radius={8}
          fillOpacity={0.6}
        />
      ));
    }
  }, [data, viewType]);

   const alertMarkers = useMemo(() => {
    return alerts.map(alert => {
      // Update .personCurrentLocation to .lat and .lng
      if (alert.personCurrentLocation && Array.isArray(alert.personCurrentLocation)) {
        alert.lat = alert.personCurrentLocation[1];
        alert.lng = alert.personCurrentLocation[0];
      }

      return (
        <CircleMarkerPopup
          key={alert.id}
          type="alert"
          data={alert}
          color={MARKER_COLORS.alert}
          fillColor={MARKER_COLORS.alert}
          radius={10}
          fillOpacity={0.2}
        />
      );
    });
  }, [alerts]);

  return (
    <MapContainer
      center={[53.37575635880662, -6.5230679512023935]}
      zoom={16}
      className="leaflet-container"
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors"
      />
      <ClickLogger />
      {renderedElements}
      {alertMarkers}
    </MapContainer>
  );
};

export default Map;

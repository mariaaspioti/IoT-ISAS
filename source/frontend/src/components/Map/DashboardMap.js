import React, { useMemo, useState, useEffect } from 'react';
import { MapContainer, TileLayer, useMapEvent, Polygon, Popup, Pane } from 'react-leaflet';
import CircleMarkerPopup from './CircleMarkerPopup';
import 'leaflet/dist/leaflet.css';
import { saveCoordinates } from '../../services/api';
import { fetchBuildingCoordinates } from '../../services/buildingService';
import { VIEW_TYPES } from '../../constants';

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
  // doors: 'green',
  doors: "#a9a9a9",
  people: 'blue',
  alert: 'red',
};

const ROLE_COLORS = {
  Engineer: 'purple',
  Janitor: 'brown',
  Technician: 'orange',
  'Cleanroom Operator': 'teal',
  Default: 'blue', // Fallback color
};

const DashboardMap = ({ 
  data, 
  viewType, 
  alerts, 
  maintenanceSchedules, 
  onDismissAlert, 
  onUnlockDoors, 
  onActivateAlarm, 
  doorStates
}) => {
  const [buildingCoordinates, setBuildingCoordinates] = useState({});

  // Memoize data layers with proper dependencies
  const buildingsData = useMemo(
    () => data[VIEW_TYPES.BUILDINGS] || [],
    [data]
  );

  const doorsData = useMemo(
    () => data[VIEW_TYPES.DOORS] || [],
    [data]
  );

  const peopleData = useMemo(
    () => data[VIEW_TYPES.PEOPLE] || [],
    [data]
  );

  // Building polygons
  const buildingElements = useMemo(() => {
    const buildingGroups = buildingsData.reduce((acc, item) => {
      const parts = item.message.split(':');
      const buildingId = parts[parts.length - 1].trim();
      (acc[buildingId] = acc[buildingId] || []).push([item.lng, item.lat, item.name]);
      return acc;
    }, {});

    return Object.entries(buildingGroups).map(([buildingId, positions]) => {
      const name = positions[0][2];
      const coordinates = positions.map(([lng, lat]) => [lat, lng]);
      return (
        <Polygon key={buildingId} positions={coordinates} color={MARKER_COLORS.buildings}>
          <Popup><strong>Building:</strong> {name}</Popup>
        </Polygon>
      );
    });
  }, [buildingsData]);

  // Door markers with state handling
  const doorElements = useMemo(() => doorsData.map(door => {
    const doorState = doorStates[door.id]?.status || 'default';
    const color = {
      success: 'blue',
      denied: 'red',
      default: MARKER_COLORS.doors,
    }[doorState];

    return (
      <CircleMarkerPopup
        key={door.id}
        type="door"
        data={door}
        color={color}
        fillColor={color}
        radius={viewType === VIEW_TYPES.PEOPLE ? (doorState === 'default' ? 3 : 10) : 5}
        fillOpacity={0.8}
      >
        {doorState !== 'default' && (
          <Popup>
            {doorState === 'success' ? '✅ Access Granted' : '⛔ Access Denied'}
          </Popup>
        )}
      </CircleMarkerPopup>
    );
  }), [doorsData, doorStates, viewType]);

  // People markers
  const peopleElements = useMemo(() => peopleData.map(person => {
    const personColor = ROLE_COLORS[person.person_role] || ROLE_COLORS.Default;
    return (
      <CircleMarkerPopup
        key={person.person_id}
        type="person"
        data={person}
        color={personColor}
        fillColor={personColor}
        radius={9}
        fillOpacity={0.8}
      />
    );
  }), [peopleData]);

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
          color={alert.status === 'resolved' ? 'green' : MARKER_COLORS.alert}
          fillColor={alert.severity === 'high' ? MARKER_COLORS.alert : 'orange'}
          radius={10}
          fillOpacity={0.2}
          onDismissAlert={onDismissAlert}
          onUnlockDoors={onUnlockDoors}
          onActivateAlarm={onActivateAlarm}
        />
      );
    });
  }, [alerts, onDismissAlert, onUnlockDoors, onActivateAlarm]);

  // Combined view logic
  const getViewElements = () => {
    switch(viewType) {
      case VIEW_TYPES.BUILDINGS:
        return buildingElements;
        
      case VIEW_TYPES.DOORS:
        return doorElements;

      case VIEW_TYPES.PEOPLE:
        return [...peopleElements, ...doorElements];

      default:
        return null;
    }
  };

  // Fetch coordinates when maintenance schedules change
  useEffect(() => {
    const fetchCoordinates = async () => {
      const coordinatesMap = {};
      for (const schedule of maintenanceSchedules) {
        try {
          const coords = await fetchBuildingCoordinates(schedule.facilityId);
          coordinatesMap[schedule.facilityId] = coords;
        } catch (error) {
          console.warn(`Using default coordinates for ${schedule.facilityId}`);
          coordinatesMap[schedule.facilityId] = []
        }
      }
      
      setBuildingCoordinates(coordinatesMap);
    };

    fetchCoordinates();
  }, [maintenanceSchedules]);

  const maintenanceOverlays = useMemo(() => {
    return maintenanceSchedules.map(schedule => {
      const coordinates = buildingCoordinates[schedule.facilityId] || []; // Use default if not found

      return (<Polygon
        key={schedule.id}
        positions={coordinates}
        color="orange"
        fillOpacity={0.2}
        pane="maintenancePane"
      >
        <Popup>
          <h3>Maintenance Scheduled</h3>
          <strong>Building:</strong> {schedule.facilityName}<br />
          <strong>Start:</strong> {new Date(schedule.startTime).toLocaleString()}<br />
          <strong>End:</strong> {new Date(schedule.endTime).toLocaleString()}<br />
          <strong>Status:</strong> {schedule.status}<br />
          <span className='description-scrooll'><strong>Description:</strong> {schedule.description}</span><br />
          <strong>Exempt Personnel:</strong> {schedule.peopleNames && schedule.peopleNames.length > 0 ? (
            <ul>
              {schedule.peopleNames.map(personName => (
                <li key={personName}>{personName}</li>
              ))}
            </ul>
          ) : (
            <span><em>None</em></span>
          )}
        </Popup>
      </Polygon>
    )});
  }, [maintenanceSchedules, buildingCoordinates]);

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
      {/* Create a custom pane for alerts */}
      <Pane name="alertPane" style={{ zIndex: 650, pointerEvents: 'none' }} />
      {/* Create a custom pane for maintenance overlays */}
      <Pane name="maintenancePane" style={{ zIndex: 600, pointerEvents: 'none' }} />
      

      <ClickLogger />
      {getViewElements()}
      {maintenanceOverlays}
      {alertMarkers}
    </MapContainer>
  );
};

export default DashboardMap;

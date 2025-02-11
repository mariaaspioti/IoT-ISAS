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

  // Use memoization for markers or polygons
  const renderedElements = useMemo(() => {
    if (viewType === 'buildings') {
      // Group building data by building id extracted from the message.
      const buildingGroups = {};
      data[viewType].forEach((item) => {
        // messages are of the form: "Building: urn:ngsi-ld:Building:<id>"
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
      // Use doorStates to change the appearance of door markers.
      return data[VIEW_TYPES.DOORS]?.map((door) => {
        // Look up the door's current state; default to 'default' if not set.
        const doorState = doorStates[door.id]?.status || 'default';
        const color = {
          success: 'blue',
          denied: 'red',
          default: MARKER_COLORS.doors,
        }[doorState];

        console.log("DoorState in DashboardMap for viewType doors", doorState);
        console.log("door in DashboardMap for viewType doors", door);

        return (
          <CircleMarkerPopup
            key={door.id}
            type="door"
            data={door}
            color={color}
            fillColor={color}
            radius={doorState === 'default' ? 3 : 5} // Larger when active (i.e. not 'default')
            fillOpacity={0.8}
          >
            {doorState !== 'default' && (
              <Popup>
                {doorState === 'success' ? '✅ Access Granted' : '⛔ Access Denied'}
              </Popup>
            )}
          </CircleMarkerPopup>
        );
      });
    } else if (viewType === 'people') {
       // Render people markers.
      const peopleMarkers = data[VIEW_TYPES.PEOPLE].map((mdata) => {
        const personColor = ROLE_COLORS[mdata.person_role] || ROLE_COLORS.Default;
        return (
          <CircleMarkerPopup
            key={mdata.person_id}
            type="person"
            data={mdata}
            color={personColor}
            fillColor={personColor}
            radius={9}
            fillOpacity={0.8}
          />
        );
      });

      // Render door markers with state-based styling (same as above).
      const doorMarkers = data[VIEW_TYPES.DOORS]?.map((door) => {
        const doorState = doorStates[door.id]?.status || 'default';
        const color = {
          success: 'blue',
          denied: 'red',
          default: MARKER_COLORS.doors,
        }[doorState];

        return (
          <CircleMarkerPopup
            key={door.message.split('Door: ')[1] || door.id}
            type="door"
            data={door}
            color={color}
            fillColor={color}
            radius={doorState === 'default' ? 3 : 5}
            fillOpacity={0.8}
          >
            {doorState !== 'default' && (
              <Popup>
                {doorState === 'success' ? '✅ Access Granted' : '⛔ Access Denied'}
              </Popup>
            )}
          </CircleMarkerPopup>
        );
      });

      return [...peopleMarkers, ...doorMarkers];
    }
  }, [data, viewType, doorStates]);

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

  // Fetch coordinates when maintenance schedules change
  useEffect(() => {
    const fetchCoordinates = async () => {
      const coordinatesMap = {};
      console.log("Maintenance schedule in useEffect of DashboardMap", maintenanceSchedules);
      for (const schedule of maintenanceSchedules) {
        try {
          console.log(`Fetching coordinates for ${schedule} in useEffect of DashboardMap`);
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
      {/* Create a custom pane for alerts */}
      <Pane name="alertPane" style={{ zIndex: 650, pointerEvents: 'none' }} />

      {/* Create a custom pane for maintenance overlays */}
      <Pane name="maintenancePane" style={{ zIndex: 600, pointerEvents: 'none' }} />
      {maintenanceOverlays}

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

export default DashboardMap;

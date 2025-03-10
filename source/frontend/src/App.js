import React, { useState, useCallback, useEffect, useMemo, useRef } from 'react';
import useWebSocket from './hooks/useWebSocket';
import useMapData from './hooks/useMapData';
import { VIEW_TYPES, MAX_ALERTS } from './constants';
import ViewControls from './components/MapControls/ViewControls';
import AlertsList from './components/Alerts/AlertsList';
import DashboardMap from './components/Map/DashboardMap';
import ScheduleMaintenance from './components/Maintenance/ScheduleMaintenance';
import MaintenanceList from './components/Maintenance/MaintenanceList';
import CameraFeed from './components/CameraFeed/CameraFeed';
import HistoricRoutesView from './components/HistoricRoutes/HistoricRoutesView';
import HandleSmartLocks from './components/SmartLocks/HandleSmartLocks';
import './App.css';

import {
  fetchFormatAlertData, fetchAllFacilitiesData, fetchAllPeopleData,
  postMaintenanceSchedule, fetchAuthorizationData, fetchScheduledMaintenanceData,
  fetchActiveAlertsData, patchUpdatedAlertStatusData, patchUpdatedAlertActionData,
  updateMaintenanceStatus
} from './services/editDashboardData';

function App() {
  // for the view controls
  const [activeView, setActiveView] = useState(VIEW_TYPES.PEOPLE);
  // for the alerts
  const [alerts, setAlerts] = useState([]);
  // for the map data
  const { loading, mapData } = useMapData();
  // for the schedule maintenance form
  const [showScheduler, setShowScheduler] = useState(false);
  // for the maintenance schedules
  const [maintenanceSchedules, setMaintenanceSchedules] = useState([]);
  // for the buildings and workers
  const [buildings, setBuildings] = useState([]);
  const [workers, setWorkers] = useState([]);
  const [doorStates, setDoorStates] = useState({});
  // for the live cameras
  const [showLiveCameras, setShowLiveCameras] = useState(false);
  // for the historic view of worker routes
  const [showHistoricRoutes, setShowHistoricRoutes] = useState(false);
  // for the smart locks
  const [showSmartLocks, setShowSmartLocks] = useState(false);

  // Load initial data
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        const [buildingsData, workersData, maintenanceData, alertsData] =
          await Promise.all([
            fetchAllFacilitiesData(),
            fetchAllPeopleData(),
            fetchScheduledMaintenanceData(),
            fetchActiveAlertsData()
          ]);

        setBuildings(buildingsData);
        setWorkers(workersData);
        setMaintenanceSchedules(maintenanceData);
        setAlerts(alertsData);
      } catch (error) {
        console.error('Initial data load error:', error);
      }
    };

    loadInitialData();
  }, []);

  const mapDataRef = useRef(mapData);
  useEffect(() => {
    mapDataRef.current = mapData;
  }, [mapData]);

  const generateAccessViolationAlert = (personId, buildingId, reason) => {
    const violationAlert = {
      id: `access-violation-${Date.now()}`,
      type: 'AccessViolation',
      personId,
      buildingId,
      description: `Unauthorized access attempt: ${reason}`,
      severity: 'high',
      timestamp: new Date().toISOString()
    };

    // setAlerts(prev => [violationAlert, ...prev].slice(0, MAX_ALERTS));
  };

  // Handle maintenance scheduling
  const handleScheduleSubmit = async (schedule) => {
    try {
      const newSchedule = await postMaintenanceSchedule(schedule);

      setMaintenanceSchedules(prev => [...prev, newSchedule]);
    } catch (error) {
      console.error('Scheduling error:', error);
    }
  };

  const handleCancelMaintenance = useCallback(async (scheduleId) => {
    try {
      await updateMaintenanceStatus(scheduleId, 'cancelled');
      // Update the schedule status to 'cancelled'
      setMaintenanceSchedules(prevSchedules => 
        prevSchedules.map(schedule =>
          schedule.id === scheduleId ? { ...schedule, status: 'cancelled' } : schedule
        )
      );

      // Remove the cancelled schedule from the frontend after 5 seconds
      const timeoutId = setTimeout(() => {
        setMaintenanceSchedules(prevSchedules => 
          prevSchedules.filter(schedule => schedule.status !== 'cancelled')
        );
      }, 5000);

      // Clear the timeout when the component unmounts
      return () => clearTimeout(timeoutId);
    } catch (error) {
      console.error('Error cancelling maintenance:', error);
    }
  }, []);

  const handleNewAlert = useCallback(async (alert) => {
    try {
      const isNew = true;
      const formattedAlert = await fetchFormatAlertData(alert, isNew);
      setAlerts(prev => [
        { ...formattedAlert, frontend_timestamp: new Date().toLocaleTimeString() },
        ...prev
      ].slice(0, MAX_ALERTS));
    } catch (error) {
      console.error('Error processing alert:', error);
    }
  }, []);

  const handleNfcDeviceUpdate = useCallback((device, result) => {
    // console.log('NFC Device Update:', device, result);
    // device is the NFC reader Device entity
    // device.controlledAsset is the controlled Smart Lock entity, so
    // device.controlledAsset == doors[device.id] which is the Smart Lock entity
    // we're interested in

    // Access doors from mapData instead of separate state
    const doors = mapDataRef.current[VIEW_TYPES.DOORS] || [];

    // Handle NGSI-LD URI format
    const targetDoorId = device.controlledAsset.value[0];

    const door = doors.find(door => door.id === targetDoorId);

    if (!door) {
      console.error('Controlled asset not found for the specified NFC reader');
      return;
    }

    setDoorStates(prev => {
      if (prev[door.id]?.timerId) {
        clearTimeout(prev[door.id].timerId);
      }

      const newState = {
        status: result,
        timerId: setTimeout(() => {
          setDoorStates(prev => ({
            ...prev,
            [door.id]: { ...prev[door.id], status: 'default' }
          }));
        }, 8000)
      };

      return { ...prev, [door.id]: newState };
    });

    if (result === 'denied') {
      generateAccessViolationAlert(device.personId, door.entry, result.reason);
    }
  }, []);



  // Add useMemo to prevent unnecessary handler recreation
  const eventHandlers = useMemo(() => ({
    alertSOSbutton: handleNewAlert,
    nfcDeviceUpdate: handleNfcDeviceUpdate
  }), [handleNewAlert, handleNfcDeviceUpdate]);

  // Update the useWebSocket usage
  useWebSocket(eventHandlers);

  // for the door states
  useEffect(() => {
    return () => {
      // Clear all timers when component unmounts
      Object.values(doorStates).forEach(state => clearTimeout(state.timerId));
    };
  }, [doorStates]);

  const handleDismissAlert = useCallback(async (alertId) => {
    // status is 'dismissed'
    const alertStatus = 'dismissed';
    setAlerts(prev => prev.map(alert =>
      alert.id === alertId ? { ...alert, status: alertStatus } : alert
    ));

    // remove from the frontend
    setAlerts(prev => prev.filter(alert => alert.id !== alertId));

    // update in the backend
    const response = await patchUpdatedAlertStatusData(alertId, alertStatus);
    if (response) {
      console.log('State updated successfully');
    }

  }, []);

  const handleUnlockDoors = useCallback(async (alertId) => {
    // status is 'resolved'
    const alertStatus = 'resolved';
    setAlerts(prev => prev.map(alert =>
      alert.id === alertId ? { ...alert, status: alertStatus } : alert
    ));

    // update in the backend
    console.log(`Unlocking doors for alert ${alertId} with status ${alertStatus}`);
    // await ---unlockDoors---
    const responseStatus = await patchUpdatedAlertStatusData(alertId, alertStatus);
    const responseAction = await patchUpdatedAlertActionData(alertId, 'unlock doors');
    if (responseStatus) {
      console.log('State updated successfully');
    }
    if (responseAction) {
      console.log('Action updated successfully');
    }
  }, []);

  const handleActivateAlarm = useCallback(async (alertId) => {
    // status is 'resolved'
    const alertStatus = 'resolved';
    setAlerts(prev => prev.map(alert =>
      alert.id === alertId ? { ...alert, status: alertStatus } : alert
    ));

    // update in the backend
    console.log(`Activating alarm for alert ${alertId}`);
    // await ---activateAlarm---
    const responseStatus = await patchUpdatedAlertStatusData(alertId, alertStatus);
    const responseAction = await patchUpdatedAlertActionData(alertId, 'activate alarm');
    if (responseStatus) {
      console.log('State updated successfully');
    }
    if (responseAction) {
      console.log('Action updated successfully');
    }
  }, []);

  // Add to your existing alert handling logic
  const checkAccessAuthorization = async (personId, buildingId) => {
    try {
      const { authorized, reason } = fetchAuthorizationData(personId, buildingId);

      if (!authorized) {
        generateAccessViolationAlert(personId, buildingId, reason);
      }
    } catch (error) {
      console.error('Access check failed:', error);
    }
  };

  const handleSmartLockAction = (data) => {
    console.log('Smart Lock Action:', data);
    // Implement the logic to handle the smart lock action
  };

  return (
    <div className="app-container">
      <div className="header-controls">
        <h1>Industrial Spatial Authorization System</h1>
      </div>

      <ViewControls
        activeView={activeView}
        setActiveView={setActiveView}
      />

      {loading ? (
        <div className="loading-container">
          <p>Loading map data...</p>
        </div>
      ) : (
        <div className="main-content">
          <div className="map-container">
            <DashboardMap
              data={mapData}
              alerts={alerts}
              maintenanceSchedules={maintenanceSchedules}
              viewType={activeView}
              onDismissAlert={handleDismissAlert}
              onUnlockDoors={handleUnlockDoors}
              onActivateAlarm={handleActivateAlarm}
              doorStates={doorStates}
            />
          </div>

          <div className="data-panels">
            <AlertsList
              alerts={alerts}
              onDismissAlert={handleDismissAlert}
              onUnlockDoors={handleUnlockDoors}
              onActivateAlarm={handleActivateAlarm}
            />
            <MaintenanceList
              maintenanceSchedules={maintenanceSchedules}
              onCancelMaintenance={handleCancelMaintenance}
            />
          </div>
        </div>
      )}

      <div className="scheduler-controls">
        <button onClick={() => setShowScheduler(!showScheduler)}>
          {showScheduler ? 'Hide Scheduler' : 'Schedule Maintenance'}
        </button>
      </div>

      {showScheduler && (
        <ScheduleMaintenance
          buildings={buildings}
          workers={workers}
          onSubmit={handleScheduleSubmit}
        />
      )}

      <div className='historic-routes-controls'>
        <button onClick={() => setShowHistoricRoutes(!showHistoricRoutes)}>
          {showHistoricRoutes ? 'Hide Historic Routes' : 'Show Historic Routes'}
        </button>
      </div>

      {showHistoricRoutes && <HistoricRoutesView
        people={workers}
      />}


      <div className="smart-locks-controls">
        <button onClick={() => setShowSmartLocks(!showSmartLocks)}>
          {showSmartLocks ? 'Hide Lock Actions' : 'Show Lock Actions'}
        </button>
      </div>

      {showSmartLocks && (
        <HandleSmartLocks onSubmit={handleSmartLockAction} />
      )}

      <div className="live-cameras-controls">
        <button onClick={() => setShowLiveCameras(!showLiveCameras)}>
          {showLiveCameras ? 'Hide Live Cameras' : 'Show Live Cameras'}
        </button>
      </div>

      {showLiveCameras && (
        <>
          <h2 className="live-cameras-header">Live Cameras</h2>
          <div className="camera-feed-grid">
            <div className="camera-feed-container">
              <div className="camera-feed">
                <h3>Cleanroom #1</h3>
                <CameraFeed />
              </div>
            </div>
            <div className="camera-feed-container">
              <div className="camera-feed">
                <h3>Cleanroom #2</h3>
                <CameraFeed />
              </div>
            </div>
            <div className="camera-feed-container">
              <div className="camera-feed">
                <h3>Cleanroom #3</h3>
                <CameraFeed />
              </div>
            </div>
            <div className="camera-feed-container">
              <div className="camera-feed">
                <h3>Cleanroom #4</h3>
                <CameraFeed />
              </div>
            </div>
          </div>
        </>
      )}


      <div className="update-notice">
        Map data updates every 2 seconds. Last update: {new Date().toLocaleTimeString()}
      </div>
    </div>
  );
}

export default App;
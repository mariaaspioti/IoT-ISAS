import React, { useState, useCallback, useEffect, useMemo } from 'react';
import useWebSocket from './hooks/useWebSocket';
import useMapData from './hooks/useMapData';
import { VIEW_TYPES, MAX_ALERTS } from './constants';
import ViewControls from './components/MapControls/ViewControls';
import AlertsList from './components/Alerts/AlertsList';
import DashboardMap from './components/Map/DashboardMap';
import ScheduleMaintenance from './components/Maintenance/ScheduleMaintenance';
import MaintenanceList from './components/Maintenance/MaintenanceList';
import './App.css';

import { fetchFormatAlertData, fetchAllFacilitiesData, fetchAllPeopleData,
  postMaintenanceSchedule, fetchAuthorizationData, fetchScheduledMaintenanceData,
  fetchActiveAlertsData, patchUpdatedAlertStatusData, patchUpdatedAlertActionData
 } from './services/editDashboardData';

function App() {
  const [activeView, setActiveView] = useState(VIEW_TYPES.BUILDINGS);
  const [alerts, setAlerts] = useState([]);
  const { loading, mapData } = useMapData();
  // for the schedule maintenance form
  const [showScheduler, setShowScheduler] = useState(false);
  const [maintenanceSchedules, setMaintenanceSchedules] = useState([]);
  const [buildings, setBuildings] = useState([]);
  const [workers, setWorkers] = useState([]);

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
          
          // console.log('Initial maintenanceData in App.js:', maintenanceData);
          console.log('Initial alertsData in App.js:', alertsData);
        setBuildings(buildingsData);
        setWorkers(workersData);
        // setMaintenanceSchedules(maintenanceData.filter(s => 
        //   new Date(s.scheduledTime) > new Date()
        // ));
        setMaintenanceSchedules(maintenanceData);
        // setAlerts(alertsData.filter(a => !a.resolved));
        setAlerts(alertsData);
      } catch (error) {
        console.error('Initial data load error:', error);
      }
    };
    
    loadInitialData();
  }, []);

  // Handle maintenance scheduling
  const handleScheduleSubmit = async (schedule) => {
    try {
      // const response = await fetch('/api/maintenance', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(schedule)
      // });
      
      // if (!response.ok) throw new Error('Scheduling failed');
      
      // const newSchedule = await response.json();
      const newSchedule = await postMaintenanceSchedule(schedule);
      console.log('New schedule:', newSchedule);

      setMaintenanceSchedules(prev => [...prev, newSchedule]);
    } catch (error) {
      console.error('Scheduling error:', error);
    }
  };

  // const handleNewAlert = useCallback(async (alert) => {
  //   try {
  //     // Process alert asynchronously first
  //     const formattedAlert = await fetchFormatAlertData(alert);
      
  //     // Then update state with processed alert
  //     setAlerts(prev => {
  //       const newAlert = {
  //         ...formattedAlert,
  //         frontend_timestamp: new Date().toLocaleTimeString()
  //       };
        
  //       // Maintain temporal order while limiting count
  //       const updated = [newAlert, ...prev];
  //       return updated.length > MAX_ALERTS 
  //         ? updated.slice(0, MAX_ALERTS)
  //         : updated;
  //     });
  //   } catch (error) {
  //     console.error('Error processing alert:', error);
  //   }
  // }, []);
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
    // Implement your NFC update logic here
    console.log('NFC Device Update:', device, result);
    // ...
  }, []);

  // Add useMemo to prevent unnecessary handler recreation
  const eventHandlers = useMemo(() => ({
    alertSOSbutton: handleNewAlert,
    nfcDeviceUpdate: handleNfcDeviceUpdate
  }), [handleNewAlert, handleNfcDeviceUpdate]);
  
  // Update the useWebSocket usage
  useWebSocket(eventHandlers);

  const handleDismissAlert = useCallback(async (alertId) => {
    // status is 'dismissed'
    const alertStatus = 'dismissed';
    setAlerts(prev => prev.map(alert =>
      alert.id === alertId ? { ...alert, status: alertStatus } : alert
    ));

    // remove from the frontend
    setAlerts(prev => prev.filter(alert => alert.id !== alertId));

    // update in the backend
    console.log(`Dismissing alert in handleDismissAlert: ${alertId}`);
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
      // const response = await fetch(`/api/access-check?person=${personId}&building=${buildingId}`);
      // const { authorized, reason } = await response.json();
      const { authorized, reason } = fetchAuthorizationData(personId, buildingId);
      
      if (!authorized) {
        generateAccessViolationAlert(personId, buildingId, reason);
      }
    } catch (error) {
      console.error('Access check failed:', error);
    }
  };

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
  
  setAlerts(prev => [violationAlert, ...prev].slice(0, MAX_ALERTS));
};

  return (
    <div className="app-container">
      <div className="header-controls">
        <h1>Industrial Spatial Authorization System</h1>
        <button onClick={() => setShowScheduler(!showScheduler)}>
          {showScheduler ? 'Hide Scheduler' : 'Schedule Maintenance'}
        </button>
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
            />
          </div>
        </div>
      )}

      {showScheduler && (
              <ScheduleMaintenance
                buildings={buildings}
                workers={workers}
                onSubmit={handleScheduleSubmit}
              />
            )}
      <div className="update-notice">
              Map data updates every 2 seconds. Last update: {new Date().toLocaleTimeString()}
            </div>
    </div>
  );
}

export default App;
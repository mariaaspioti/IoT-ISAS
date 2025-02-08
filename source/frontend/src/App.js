import React, { useState, useCallback, useEffect } from 'react';
import useWebSocket from './hooks/useWebSocket';
import useMapData from './hooks/useMapData';
import { VIEW_TYPES, MAX_ALERTS } from './constants';
import ViewControls from './components/MapControls/ViewControls';
import AlertsList from './components/Alerts/AlertsList';
import DashboardMap from './components/Map/DashboardMap';
import ScheduleMaintenance from './components/Maintenance/ScheduleMaintenance';
import './App.css';

import { fetchFormatAlertData, fetchAllFacilitiesData, fetchAllPeopleData,
  postMaintenanceSchedule, fetchAuthorizationData
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
      const buildingsData = await fetchAllFacilitiesData();
      const workersData = await fetchAllPeopleData();
      setBuildings(buildingsData);
      setWorkers(workersData);
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

  const handleNewAlert = useCallback(async (alert) => {
    try {
      // Process alert asynchronously first
      const formattedAlert = await fetchFormatAlertData(alert);
      
      // Then update state with processed alert
      setAlerts(prev => {
        const newAlert = {
          ...formattedAlert,
          frontend_timestamp: new Date().toLocaleTimeString()
        };
        
        // Maintain temporal order while limiting count
        const updated = [newAlert, ...prev];
        return updated.length > MAX_ALERTS 
          ? updated.slice(0, MAX_ALERTS)
          : updated;
      });
    } catch (error) {
      console.error('Error processing alert:', error);
    }
  }, []);

  useWebSocket(handleNewAlert);

  const handleDismissAlert = useCallback((alertId) => {
    setAlerts(prev => prev.filter(alert => alert.id !== alertId));
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

      {showScheduler && (
              <ScheduleMaintenance
                buildings={buildings}
                workers={workers}
                onSubmit={handleScheduleSubmit}
              />
            )}
      
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
            data={mapData[activeView]} 
            alerts={alerts}
            maintenanceSchedules={maintenanceSchedules} 
            viewType={activeView}
            onDismissAlert={handleDismissAlert}
             />
            <div className="update-notice">
              Data updates every 2 seconds. Last update: {new Date().toLocaleTimeString()}
            </div>
          </div>

          <AlertsList 
          alerts={alerts}
          onDismissAlert={handleDismissAlert}
           />
        </div>
      )}

      {/* {showScheduler && (
              <ScheduleMaintenance
                buildings={buildings}
                workers={workers}
                onSubmit={handleScheduleSubmit}
              />
            )} */}
    </div>
  );
}

export default App;
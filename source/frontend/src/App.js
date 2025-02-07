import React, { useState, useCallback } from 'react';
import useWebSocket from './hooks/useWebSocket';
import useMapData from './hooks/useMapData';
import { VIEW_TYPES, MAX_ALERTS } from './constants';
import ViewControls from './components/MapControls/ViewControls';
import AlertsList from './components/Alerts/AlertsList';
import Map from './components/Map/Map';
import './App.css';

import { fetchFormatAlertData } from './services/editDashboardData';

function App() {
  const [activeView, setActiveView] = useState(VIEW_TYPES.BUILDINGS);
  const [alerts, setAlerts] = useState([]);
  const { loading, mapData } = useMapData();

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

  return (
    <div className="app-container">
      <h1>Industrial Spatial Authorization System</h1>
      
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
            <Map data={mapData[activeView]} alerts={alerts} viewType={activeView} />
            <div className="update-notice">
              Data updates every 2 seconds. Last update: {new Date().toLocaleTimeString()}
            </div>
          </div>

          <AlertsList alerts={alerts} />
        </div>
      )}
    </div>
  );
}

export default App;
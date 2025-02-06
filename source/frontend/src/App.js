import React, { useState, useEffect, useCallback } from 'react';
import './App.css';
import Map from './components/Map';
import * as editMap from './services/editMap';

// View types enumeration for better type safety
const VIEW_TYPES = {
  BUILDINGS: 'buildings',
  DOORS: 'doors',
  PEOPLE: 'people'
};

function App() {
  const [loading, setLoading] = useState(true);
  const [activeView, setActiveView] = useState(VIEW_TYPES.BUILDINGS);
  const [mapData, setMapData] = useState({
    [VIEW_TYPES.BUILDINGS]: [],
    [VIEW_TYPES.DOORS]: [],
    [VIEW_TYPES.PEOPLE]: []
  });

  // Memoized fetch function to prevent unnecessary re-renders
  const fetchData = useCallback(async () => {
    try {
      const { mapData, ...rest } = await editMap.fetchTrackingData();
      const doors = await editMap.showDoors();
      const buildings = await editMap.showBuildings();
    //   console.log("Building Data:", buildings);
    //   console.log("Building Data", JSON.stringify(buildings, null, 2));
      const people = mapData;
    //   console.log("Data:", mapData, facilities, controlledAssets, data);
    //   console.log("Doors:", doors);
    //   console.log("Buildings:", buildings);
      
      setMapData(prev => ({
        [VIEW_TYPES.BUILDINGS]: buildings || prev[VIEW_TYPES.BUILDINGS],
        [VIEW_TYPES.DOORS]: doors || prev[VIEW_TYPES.DOORS],
        [VIEW_TYPES.PEOPLE]: people || prev[VIEW_TYPES.PEOPLE]
      }));
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, [fetchData]);

  const getButtonStyle = (viewType) => ({
    margin: '0 10px',
    padding: '10px 20px',
    backgroundColor: activeView === viewType ? '#007bff' : '#6c757d',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    transition: 'background-color 0.3s'
  });

  return (
    <div className="app-container">
      <h1>Industrial Spatial Authorization System</h1>
      <div className="controls">
        <button 
          style={getButtonStyle(VIEW_TYPES.BUILDINGS)}
          onClick={() => setActiveView(VIEW_TYPES.BUILDINGS)}
        >
          Show Buildings
        </button>
        <button
          style={getButtonStyle(VIEW_TYPES.DOORS)}
          onClick={() => setActiveView(VIEW_TYPES.DOORS)}
        >
          Show Doors
        </button>
        <button
          style={getButtonStyle(VIEW_TYPES.PEOPLE)}
          onClick={() => setActiveView(VIEW_TYPES.PEOPLE)}
        >
          Show People
        </button>
      </div>

      {loading ? (
        <div className="loading-container">
          <p>Loading map data...</p>
        </div>
      ) : (
        <div className="map-container">
          <Map data={mapData[activeView]} viewType={activeView} />
          <div className="update-notice">
            Data updates every 2 seconds. Last update: {new Date().toLocaleTimeString()}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
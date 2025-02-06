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

  // const handleNewAlert = useCallback((alert) => {
  //   setAlerts(prevAlerts => { 
  //     // const newAlert = {
  //     //   ...alert,
  //     //   frontend_timestamp: new Date().toLocaleTimeString()
  //     // };
  //     const newAlert = fetchFormatAlertData(alert);
  //     return [newAlert, ...prevAlerts].slice(0, MAX_ALERTS);
  //   });
  // }, []);
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
            <Map data={mapData[activeView]} viewType={activeView} />
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



//===========================================================
//===========================================================

// import React, { useState, useEffect, useCallback } from 'react';
// import io from 'socket.io-client';
// import './App.css';
// import Map from './components/Map';
// import * as editMap from './services/editMap';

// const SOCKET_SERVER_URL = 'http://localhost:3001';
// const MAX_ALERTS = 10; // Maximum number of alerts to show
// // const ALERT_TIMEOUT = 30000; // 30 seconds

// const VIEW_TYPES = {
//   BUILDINGS: 'buildings',
//   DOORS: 'doors',
//   PEOPLE: 'people'
// };

// function App() {
//   const [loading, setLoading] = useState(true);
//   const [activeView, setActiveView] = useState(VIEW_TYPES.BUILDINGS);
//   const [mapData, setMapData] = useState({
//     [VIEW_TYPES.BUILDINGS]: [],
//     [VIEW_TYPES.DOORS]: [],
//     [VIEW_TYPES.PEOPLE]: []
//   });
//   const [alerts, setAlerts] = useState([]);

//   // Memoized fetch function
//   const fetchData = useCallback(async () => {
//     try {
//       const { mapData, ...rest } = await editMap.fetchTrackingData();
//       const doors = await editMap.showDoors();
//       const buildings = await editMap.showBuildings();
      
//       setMapData(prev => ({
//         [VIEW_TYPES.BUILDINGS]: buildings || prev[VIEW_TYPES.BUILDINGS],
//         [VIEW_TYPES.DOORS]: doors || prev[VIEW_TYPES.DOORS],
//         [VIEW_TYPES.PEOPLE]: mapData || prev[VIEW_TYPES.PEOPLE]
//       }));
//       setLoading(false);
//     } catch (error) {
//       console.error('Error fetching data:', error);
//       setLoading(false);
//     }
//   }, []);

//   // Handle new alerts
//   const handleNewAlert = useCallback((alert) => {
//     setAlerts(prevAlerts => {
//       const newAlert = {
//         ...alert,
//         frontend_timestamp: new Date().toLocaleTimeString()
//       };
//       return [newAlert, ...prevAlerts].slice(0, MAX_ALERTS);
//     });
//   }, []);

//   // Auto-remove old alerts
// //   useEffect(() => {
// //     const timer = setInterval(() => {
// //       setAlerts(prev => prev.filter(alert => 
// //         Date.now() - alert.id < ALERT_TIMEOUT
// //       ));
// //     }, 1000);

// //     return () => clearInterval(timer);
// //   }, []);

//   // WebSocket setup
//   const connectSocket = useCallback(() => {
//     const socket = io(SOCKET_SERVER_URL);

//     socket.on('connect', () => {
//       console.log('Connected to Socket.IO server');
//     });

//     socket.on('alertSOSbutton', handleNewAlert);

//     socket.on('disconnect', () => {
//       console.log('Disconnected from Socket.IO server');
//     });

//     return socket;
//   }, [handleNewAlert]);

//   useEffect(() => {
//     const socket = connectSocket();
//     fetchData();
//     const interval = setInterval(fetchData, 2000);
    
//     return () => {
//       socket.disconnect();
//       clearInterval(interval);
//     };
//   }, [connectSocket, fetchData]);

//   const getButtonStyle = (viewType) => ({
//     margin: '0 10px',
//     padding: '10px 20px',
//     backgroundColor: activeView === viewType ? '#007bff' : '#6c757d',
//     color: 'white',
//     border: 'none',
//     borderRadius: '5px',
//     cursor: 'pointer',
//     transition: 'background-color 0.3s'
//   });

//   return (
//     <div className="app-container">
//       <h1>Industrial Spatial Authorization System</h1>
      
//       <div className="controls">
//         <button 
//           style={getButtonStyle(VIEW_TYPES.BUILDINGS)}
//           onClick={() => setActiveView(VIEW_TYPES.BUILDINGS)}
//         >
//           Show Buildings
//         </button>
//         <button
//           style={getButtonStyle(VIEW_TYPES.DOORS)}
//           onClick={() => setActiveView(VIEW_TYPES.DOORS)}
//         >
//           Show Doors
//         </button>
//         <button
//           style={getButtonStyle(VIEW_TYPES.PEOPLE)}
//           onClick={() => setActiveView(VIEW_TYPES.PEOPLE)}
//         >
//           Show People
//         </button>
//       </div>

//       {loading ? (
//         <div className="loading-container">
//           <p>Loading map data...</p>
//         </div>
//       ) : (
//         <>
//             <div className="main-content">
//                 <div className="map-container">
//                     <Map data={mapData[activeView]} viewType={activeView} />
//                     <div className="update-notice">
//                     Data updates every 2 seconds. Last update: {new Date().toLocaleTimeString()}
//                     </div>
//                 </div>

//                 <div className="alerts-container">
//                     <h3>Active Alerts ({alerts.length})</h3>
//                     <div className="alerts-list">
//                     {alerts.map(alert => (
//                         <div key={alert.id} className="alert-item">
//                         <div className="alert-header">
//                             <span className="alert-id">Alert #{alert.id}</span>
//                             <span className="alert-time">{alert.frontend_timestamp}</span>
//                         </div>
//                         <div className="alert-body">
//                             <span className="alert-severity">{alert.severity.value}</span>
//                             <p className="alert-description">{alert.description.value}</p>
//                         </div>
//                         </div>
//                     ))}
//                     {alerts.length === 0 && (
//                         <div className="no-alerts">No active alerts</div>
//                     )}
//                     </div>
//                 </div>
//             </div>
//         </>
//       )}
//     </div>
//   );
// }


//===========================================================
//===========================================================

// export default App;

// import React, { useState, useEffect, useCallback } from 'react';
// import io from 'socket.io-client';
// import './App.css';
// import Map from './components/Map';
// import * as editMap from './services/editMap';

// const SOCKET_SERVER_URL = 'http://localhost:3001';

// // View types enumeration for better type safety
// const VIEW_TYPES = {
//   BUILDINGS: 'buildings',
//   DOORS: 'doors',
//   PEOPLE: 'people'
// };

// function App() {
//   const [loading, setLoading] = useState(true);
//   const [activeView, setActiveView] = useState(VIEW_TYPES.BUILDINGS);
//   const [mapData, setMapData] = useState({
//     [VIEW_TYPES.BUILDINGS]: [],
//     [VIEW_TYPES.DOORS]: [],
//     [VIEW_TYPES.PEOPLE]: []
//   });

//   // Memoized fetch function to prevent unnecessary re-renders
//   const fetchData = useCallback(async () => {
//     try {
//       const { mapData, ...rest } = await editMap.fetchTrackingData();
//       const doors = await editMap.showDoors();
//       const buildings = await editMap.showBuildings();
//     //   console.log("Building Data:", buildings);
//     //   console.log("Building Data", JSON.stringify(buildings, null, 2));
//       const people = mapData;
//     //   console.log("Data:", mapData, facilities, controlledAssets, data);
//     //   console.log("Doors:", doors);
//     //   console.log("Buildings:", buildings);
      
//       setMapData(prev => ({
//         [VIEW_TYPES.BUILDINGS]: buildings || prev[VIEW_TYPES.BUILDINGS],
//         [VIEW_TYPES.DOORS]: doors || prev[VIEW_TYPES.DOORS],
//         [VIEW_TYPES.PEOPLE]: people || prev[VIEW_TYPES.PEOPLE]
//       }));
//       setLoading(false);
//     } catch (error) {
//       console.error('Error fetching data:', error);
//       setLoading(false);
//     }
//   }, []);

//   // Connect to the Socket.IO server
//   const connectSocket = () => {
//     const socket = io(SOCKET_SERVER_URL);
//     socket.on('connect', () => {
//       console.log('Connected to the Socket.IO server');
//     });

//     socket.on('disconnect', () => {
//       console.log('Disconnected from the Socket.IO server');
//     });

//     socket.on('alertSOSbutton', (alert) => {
//       console.log('Received new alert:', alert);
//     });

//     return socket;
//   };

//   useEffect(() => {
//     const socket = connectSocket();
//     fetchData();
//     const interval = setInterval(fetchData, 2000);
//     return () => {
//         socket.disconnect();
//         clearInterval(interval);
//     }
//   }, [fetchData]);

//   const getButtonStyle = (viewType) => ({
//     margin: '0 10px',
//     padding: '10px 20px',
//     backgroundColor: activeView === viewType ? '#007bff' : '#6c757d',
//     color: 'white',
//     border: 'none',
//     borderRadius: '5px',
//     cursor: 'pointer',
//     transition: 'background-color 0.3s'
//   });

//   return (
//     <div className="app-container">
//       <h1>Industrial Spatial Authorization System</h1>
//       <div className="controls">
//         <button 
//           style={getButtonStyle(VIEW_TYPES.BUILDINGS)}
//           onClick={() => setActiveView(VIEW_TYPES.BUILDINGS)}
//         >
//           Show Buildings
//         </button>
//         <button
//           style={getButtonStyle(VIEW_TYPES.DOORS)}
//           onClick={() => setActiveView(VIEW_TYPES.DOORS)}
//         >
//           Show Doors
//         </button>
//         <button
//           style={getButtonStyle(VIEW_TYPES.PEOPLE)}
//           onClick={() => setActiveView(VIEW_TYPES.PEOPLE)}
//         >
//           Show People
//         </button>
//       </div>

//       {loading ? (
//         <div className="loading-container">
//           <p>Loading map data...</p>
//         </div>
//       ) : (
//         <div className="map-container">
//           <Map data={mapData[activeView]} viewType={activeView} />
//           <div className="update-notice">
//             Data updates every 2 seconds. Last update: {new Date().toLocaleTimeString()}
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;
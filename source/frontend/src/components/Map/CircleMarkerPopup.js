import React, { useRef, useEffect, useState } from 'react';
import { CircleMarker, Polyline, Popup, Tooltip } from 'react-leaflet';

// Trail settings
const TRAIL_DURATION = 25000;  // How long a trail segment stays visible
const SMOOTHING_FACTOR = 1;   // Number of positions to average for smoothing
const INTERPOLATION_STEPS = 5; // Extra points per segment to smooth motion

const CircleMarkerPopup = ({ 
  type, 
  data, 
  color, 
  fillColor, 
  radius, 
  fillOpacity, 
  onDismissAlert, 
  onUnlockDoors, 
  onActivateAlarm }) => {

  const markerRef = useRef(null);
  const [popupOpen, setPopupOpen] = useState(false);
  const [trail, setTrail] = useState([]); // Store past positions

  useEffect(() => {
        if (markerRef.current) {
          const marker = markerRef.current;
          const onPopupOpen = () => setPopupOpen(true);
          const onPopupClose = () => setPopupOpen(false);
    
          marker.on('popupopen', onPopupOpen);
          marker.on('popupclose', onPopupClose);
    
          return () => {
            marker.off('popupopen', onPopupOpen);
            marker.off('popupclose', onPopupClose);
          };
        }
    }, []);
      

  useEffect(() => {
    if (markerRef.current) {
      markerRef.current.setLatLng([data.lat, data.lng]);
      if (popupOpen) markerRef.current.openPopup();
    }

    // Append new position with a timestamp
    setTrail(prevTrail => [...prevTrail, { lat: data.lat, lng: data.lng, time: Date.now() }]);
  }, [data.lat, data.lng, popupOpen]);

  // Remove old trail points over time
  useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();
      setTrail(prevTrail => prevTrail.filter(point => now - point.time < TRAIL_DURATION));
    }, 100); // Update every 100ms

    return () => clearInterval(interval);
  }, []);

  // Function to calculate a simple moving average for smoothing
  const getSmoothedTrail = (points, smoothingFactor) => {
    if (points.length < smoothingFactor) return points;
    return points.map((_, i, arr) => {
      const start = Math.max(0, i - smoothingFactor + 1);
      const slice = arr.slice(start, i + 1);
      const avgLat = slice.reduce((sum, p) => sum + p.lat, 0) / slice.length;
      const avgLng = slice.reduce((sum, p) => sum + p.lng, 0) / slice.length;
      return { lat: avgLat, lng: avgLng, time: arr[i].time };
    });
  };

  // Function to interpolate extra points between two trail points
  const interpolatePoints = (pointA, pointB, steps) => {
    const interpolated = [];
    for (let i = 1; i <= steps; i++) {
      const t = i / (steps + 1);
      interpolated.push({
        lat: pointA.lat + t * (pointB.lat - pointA.lat),
        lng: pointA.lng + t * (pointB.lng - pointA.lng),
        time: pointA.time + t * (pointB.time - pointA.time)
      });
    }
    return interpolated;
  };

  // Apply smoothing and interpolation
  const smoothedTrail = getSmoothedTrail(trail, SMOOTHING_FACTOR);
  const interpolatedTrail = [];
  for (let i = 1; i < smoothedTrail.length; i++) {
    interpolatedTrail.push(smoothedTrail[i - 1]);
    interpolatedTrail.push(...interpolatePoints(smoothedTrail[i - 1], smoothedTrail[i], INTERPOLATION_STEPS));
  }
  interpolatedTrail.push(smoothedTrail[smoothedTrail.length - 1]);

  // Create fading polyline segments
  const polylineSegments = [];
  for (let i = 1; i < interpolatedTrail.length; i++) {
    const pointA = interpolatedTrail[i - 1];
    const pointB = interpolatedTrail[i];
    const age = Date.now() - pointB.time;
    const opacity = Math.max(0, 0.9 - age / TRAIL_DURATION); // Fades over time

    if (opacity > 0) {
      polylineSegments.push(
        <Polyline
          key={`segment-${i}`}
          positions={[
            [pointA.lat, pointA.lng],
            [pointB.lat, pointB.lng]
          ]}
          pathOptions={{
            color: color,
            weight: 8, // Adjust line thickness
            opacity: opacity, // Apply fading effect
          }}
        />
      );
    }
  }

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
        <strong>Role:</strong> {data.person_role}
        <br />
        <strong>Current Facility:</strong> {data.facility_name}
        <br />
        <strong>Tracking Method:</strong> {data.tracking_type}
        <br />
        <strong>Message:</strong> {data.message || 'No message'}
      </>
    );
  } else if (type === 'alert') {
    const coordinates = data.personCurrentLocation && Array.isArray(data.personCurrentLocation)
      ? `${data.personCurrentLocation[0]}, ${data.personCurrentLocation[1]}`
      : `${data.lat}, ${data.lng}`;
    popupContent = (
      <>
        <strong>Alert:</strong> {data.description || 'No message'}
        <br />
        <strong>Time:</strong> {data.dateIssued}
        <br />
        <strong>Status:</strong> {data.status}
        <br />
        <strong>Owner:</strong> {data.personName}
        <br />
        <strong>Coordinates:</strong> {coordinates}
        <div className="alert-actions">
          <select 
            onChange={(e) => {
              if (e.target.value === 'dismiss') {
                onDismissAlert(data.id);
              }
              else if (e.target.value === 'unlock') {
                // console.log(`Unlocking doors for alert ${alertId}`);
                onUnlockDoors(data.id);
              }
              else if (e.target.value === 'alarm') {
                // console.log(`Activating alarm for alert ${alertId}`);
                onActivateAlarm(data.id);
              }
              else {
                console.log('Invalid action');
              }
              e.target.value = '';
            }}
            disabled={data.status === 'resolved'}
          >
            <option value="">Actions...</option>
            <option value="unlock">Unlock all doors</option>
            <option value="alarm">Activate Alarm</option>
            <option value="dismiss">Dismiss</option>
          </select>
        </div>
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
    <>
      {polylineSegments}

      <CircleMarker
        ref={markerRef}
        center={[data.lat, data.lng]}
        color={color}
        fillColor={fillColor}
        radius={radius}
        fillOpacity={fillOpacity}
        pane={type === 'alert' ? 'alertPane' : undefined}
        zIndexOffset={type === 'alert' ? 1000 : 0}
      >
        <Popup>{popupContent}</Popup>
        <Tooltip
          direction="bottom"
          offset={[0, 8]}
          opacity={1}
          className="marker-label"
        >
          {data.person_id ? data.person_id : data.message}
        </Tooltip>
      </CircleMarker>
    </>
  );
};

export default CircleMarkerPopup;


// ======================= GRADIENT TRAIL ======================= //

// import React, { useRef, useEffect, useState } from 'react';
// import { CircleMarker, Polyline, Popup, Tooltip } from 'react-leaflet';

// // Trail duration in milliseconds (how long each segment remains visible)
// const TRAIL_DURATION = 30000;

// const CircleMarkerPopup = ({ type, data, color, fillColor, radius, fillOpacity, onDismissAlert }) => {
//   const markerRef = useRef(null);
//   const [popupOpen, setPopupOpen] = useState(false);
//   const [trail, setTrail] = useState([]); // Store past positions

//   useEffect(() => {
//     if (markerRef.current) {
//       const marker = markerRef.current;
//       const onPopupOpen = () => setPopupOpen(true);
//       const onPopupClose = () => setPopupOpen(false);

//       marker.on('popupopen', onPopupOpen);
//       marker.on('popupclose', onPopupClose);

//       return () => {
//         marker.off('popupopen', onPopupOpen);
//         marker.off('popupclose', onPopupClose);
//       };
//     }
//   }, []);

//   // Update the marker's position and add a new trail point
//   useEffect(() => {
//     if (markerRef.current) {
//       markerRef.current.setLatLng([data.lat, data.lng]);
//       if (popupOpen) {
//         markerRef.current.openPopup();
//       }
//     }
//     // Append the new position with a timestamp
//     setTrail(prevTrail => [...prevTrail, { lat: data.lat, lng: data.lng, time: Date.now() }]);
//   }, [data.lat, data.lng, popupOpen]);

//   // Remove old trail points over time
//   useEffect(() => {
//     const interval = setInterval(() => {
//       const now = Date.now();
//       setTrail(prevTrail =>
//         prevTrail.filter(point => now - point.time < TRAIL_DURATION)
//       );
//     }, 100); // Update every 100ms

//     return () => clearInterval(interval);
//   }, []);

//   // Convert trail points into fading polyline segments
//   const polylineSegments = [];
//   for (let i = 1; i < trail.length; i++) {
//     const pointA = trail[i - 1];
//     const pointB = trail[i];
//     const age = Date.now() - pointB.time;
//     const opacity = Math.max(0, 1 - age / TRAIL_DURATION); // Opacity decreases over time

//     if (opacity > 0) {
//       polylineSegments.push(
//         <Polyline
//           key={`segment-${i}`}
//           positions={[
//             [pointA.lat, pointA.lng],
//             [pointB.lat, pointB.lng]
//           ]}
//           pathOptions={{
//             color: color,
//             weight: 6, // Adjust line thickness
//             opacity: opacity, // Apply fading effect
//           }}
//         />
//       );
//     }
//   }

//   // Define the popup content
//   let popupContent;
//   if (type === 'door') {
//     popupContent = <strong>{data.message}</strong>;
//   } else if (type === 'person') {
//     popupContent = (
//       <>
//         <strong>Coordinates:</strong> {data.lat}, {data.lng}
//         <br />
//         <strong>Belongs To:</strong> {data.person_name}
//         <br />
//         <strong>Current Facility:</strong> {data.facility_name}
//         <br />
//         <strong>Tracking Method:</strong> {data.tracking_type}
//         <br />
//         <strong>Message:</strong> {data.message || 'No message'}
//       </>
//     );
//   } else if (type === 'alert') {
//     const coordinates = data.personCurrentLocation && Array.isArray(data.personCurrentLocation)
//       ? `${data.personCurrentLocation[0]}, ${data.personCurrentLocation[1]}`
//       : `${data.lat}, ${data.lng}`;
//     popupContent = (
//       <>
//         <strong>Alert:</strong> {data.description || 'No message'}
//         <br />
//         <strong>Time:</strong> {data.frontend_timestamp}
//         <br />
//         <strong>Status:</strong> {data.status}
//         <br />
//         <strong>Owner:</strong> {data.personName}
//         <br />
//         <strong>Coordinates:</strong> {coordinates}
//         <div className="alert-actions">
//           <select 
//             onChange={(e) => {
//               if (e.target.value === 'dismiss') {
//                 onDismissAlert(data.id);
//               }
//               e.target.value = '';
//             }}
//           >
//             <option value="">Actions...</option>
//             <option value="unlock">Unlock all doors</option>
//             <option value="alarm">Activate Alarm</option>
//             <option value="dismiss">Dismiss</option>
//           </select>
//         </div>
//       </>
//     );
//   } else {
//     popupContent = (
//       <>
//         <strong>Coordinates:</strong> {data.lat}, {data.lng}
//         <br />
//         <strong>Message:</strong> {data.message || 'No message'}
//       </>
//     );
//   }

//   return (
//     <>
//       {/* Render the fading polyline trail */}
//       {polylineSegments}

//       {/* Render the moving marker */}
//       <CircleMarker
//         ref={markerRef}
//         center={[data.lat, data.lng]}
//         color={color}
//         fillColor={fillColor}
//         radius={radius}
//         fillOpacity={fillOpacity}
//         pane={type === 'alert' ? 'alertPane' : undefined}
//         zIndexOffset={type === 'alert' ? 1000 : 0}
//       >
//         <Popup>{popupContent}</Popup>
//         <Tooltip
//           direction="bottom"
//           offset={[0, 4]}
//           opacity={1}
//           className="marker-label"
//         >
//           {data.person_id ? data.person_id : data.message}
//         </Tooltip>
//       </CircleMarker>
//     </>
//   );
// };

// export default CircleMarkerPopup;


// ================================== GHOST MARKERS TRAIL ====================================== //

// import React, { useRef, useEffect, useState } from 'react';
// import { CircleMarker, Popup, Tooltip} from 'react-leaflet';

// // Duration (in milliseconds) for which a trail point remains visible.
// const TRAIL_DURATION = 3000;

// const CircleMarkerPopup = ({ type, data, color, fillColor, radius, fillOpacity, onDismissAlert }) => {
//   const markerRef = useRef(null);
//   const [popupOpen, setPopupOpen] = useState(false);
//   const [trail, setTrail] = useState([]);

//   // Set up event listeners to track popup open/close
//   useEffect(() => {
//     if (markerRef.current) {
//       const marker = markerRef.current;
//       const onPopupOpen = () => setPopupOpen(true);
//       const onPopupClose = () => setPopupOpen(false);

//       marker.on('popupopen', onPopupOpen);
//       marker.on('popupclose', onPopupClose);

//       // Cleanup when component unmounts
//       return () => {
//         marker.off('popupopen', onPopupOpen);
//         marker.off('popupclose', onPopupClose);
//       };
//     }
//   }, []);

//   // When data changes, update the marker position in place.
//   useEffect(() => {
//     if (markerRef.current) {
//       markerRef.current.setLatLng([data.lat, data.lng]);
//       // If the popup was open, re-open it after updating the position.
//       if (popupOpen) {
//         markerRef.current.openPopup();
//       }
//     }
//   }, [data.lat, data.lng, popupOpen]);

//   // Update marker position and add a new trail point when the data changes.
//   useEffect(() => {
//     if (markerRef.current) {
//       // Update the marker's position.
//       markerRef.current.setLatLng([data.lat, data.lng]);
//       if (popupOpen) {
//         markerRef.current.openPopup();
//       }
//     }
//     // Append the new position with a timestamp to the trail.
//     setTrail(prevTrail => [...prevTrail, { lat: data.lat, lng: data.lng, time: Date.now() }]);
//   }, [data.lat, data.lng, popupOpen]);
  

//   // Regularly remove trail points that have exceeded the trail duration.
//   useEffect(() => {
//     const interval = setInterval(() => {
//       const now = Date.now();
//       setTrail(prevTrail =>
//         prevTrail.filter(point => now - point.time < TRAIL_DURATION)
//       );
//     }, 100); // Update every 100ms
//     return () => clearInterval(interval);
//   }, []);

//   // Render each trail point with an opacity based on its age.
//   const trailMarkers = trail.map((point, index) => {
//     const age = Date.now() - point.time;
//     // Calculate opacity so that it fades from 1 to 0 over TRAIL_DURATION.
//     const opacity = Math.max(0, 1 - age / TRAIL_DURATION);
//     return (
//       <CircleMarker
//         key={`trail-${index}`}
//         center={[point.lat, point.lng]}
//         radius={radius}
//         pathOptions={{
//           color: color,
//           fillColor: fillColor,
//           fillOpacity: opacity,
//           opacity: opacity
//         }}
//         interactive={false} // Prevent the trail markers from being interactive
//       />
//     );
//   });

//   let popupContent;
//   if (type === 'door') {
//     popupContent = <strong>{data.message}</strong>;
//   } else if (type === 'person') {
//     popupContent = (
//       <>
//         <strong>Coordinates:</strong> {data.lat}, {data.lng}
//         <br />
//         <strong>Belongs To:</strong> {data.person_name}
//         <br />
//         <strong>Current Facility:</strong> {data.facility_name}
//         <br />
//         <strong>Tracking Method:</strong> {data.tracking_type}
//         <br />
//         <strong>Message:</strong> {data.message || 'No message'}
//       </>
//     );
//   } else if (type === 'alert') {
//     // console.log("data in CircleMarkerPopup type alert:", data);
//     const coordinates = data.personCurrentLocation && Array.isArray(data.personCurrentLocation)
//       ? `${data.personCurrentLocation[0]}, ${data.personCurrentLocation[1]}`
//       : `${data.lat}, ${data.lng}`;
//     popupContent = (
//       <>
//         <strong>Alert:</strong> {data.description || 'No message'}
//         <br />
//         <strong>Time:</strong> {data.frontend_timestamp}
//         <br />
//         <strong>Status:</strong> {data.status}
//         <br />
//         <strong>Owner:</strong> {data.personName}
//         <br />
//         <strong>Coordinates:</strong> {coordinates}
//         <div className="alert-actions">
//           <select 
//             onChange={(e) => {
//               if (e.target.value === 'dismiss') {
//                 onDismissAlert(data.id);
//               }
//               e.target.value = '';
//             }}
//           >
//             <option value="">Actions...</option>
//             <option value="unlock">Unlock all doors</option>
//             <option value="alarm">Activate Alarm</option>
//             <option value="dismiss">Dismiss</option>
//           </select>
//         </div>
//       </>
//     );
//   } else {
//     popupContent = (
//       <>
//         <strong>Coordinates:</strong> {data.lat}, {data.lng}
//         <br />
//         <strong>Message:</strong> {data.message || 'No message'}
//       </>
//     );
//   }

//   return (
//     <>
//       {/* Render the vanishing trail behind the moving marker */}
//       {trailMarkers}
//       <CircleMarker
//         ref={markerRef}
//         center={[data.lat, data.lng]}
//         color={color}
//         fillColor={fillColor}
//         radius={radius}
//         fillOpacity={fillOpacity}
//         pane={type === 'alert' ? 'alertPane' : undefined} // Use custom pane for alert markers
//         zIndexOffset={type === 'alert' ? 1000 : 0} // Higher zIndexOffset for alert markers
//       >
//         <Popup>{popupContent}</Popup>
//         <Tooltip
//           direction="bottom"
//           offset={[0, 4]}
//           opacity={1}
//           // permanent // Make the label always visible
//           className="marker-label"
//         >
//           {data.person_id ? data.person_id : data.message}
//         </Tooltip>
//       </CircleMarker>
//     </>
//   );
// };

// export default CircleMarkerPopup;
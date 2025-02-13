import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Polyline } from 'react-leaflet';
import Slider from 'rc-slider';
import DatePicker from 'react-datepicker';
import 'rc-slider/assets/index.css';
import 'react-datepicker/dist/react-datepicker.css';
import 'leaflet/dist/leaflet.css';
import './HistoricRoutesView.css';

const HistoricRoutesView = ({ people }) => {
  const [historicRoutes, setHistoricRoutes] = useState([]);
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [selectedPerson, setSelectedPerson] = useState(people.length > 0 ? people[0].id : null);
  const [timeRange, setTimeRange] = useState([0, 0]);
  const [minTime, setMinTime] = useState(null);
  const [maxTime, setMaxTime] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedTimeSpan, setSelectedTimeSpan] = useState('full_day'); // Default view

  useEffect(() => {
    const fetchHistoricData = async () => {
      if (!selectedPerson) return;

      setLoading(true);
      try {
        const dateStr = selectedDate.toISOString().split('T')[0];
        const response = await fetch(`/api/historic-tracking?date=${dateStr}&person_id=${selectedPerson}`);
        const data = await response.json();

        if (!Array.isArray(data)) {
          console.error('Unexpected response format:', data);
          setHistoricRoutes([]);
          return;
        }

        const routes = data.map(item => ({
          ...item,
          timestamp: new Date(item.timestamp).getTime(),
        }));

        setHistoricRoutes(routes);
      } catch (error) {
        console.error('Error fetching historic routes:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchHistoricData();
  }, [selectedDate, selectedPerson]);

  useEffect(() => {
    const startOfDay = new Date(selectedDate);
    startOfDay.setHours(0, 0, 0, 0);
    const endOfDay = new Date(selectedDate);
    endOfDay.setHours(23, 59, 59, 999);

    let newMinTime = startOfDay.getTime();
    let newMaxTime = endOfDay.getTime();

    // Adjust time range based on selected span
    if (selectedTimeSpan === 'morning_shift') {
      newMinTime = startOfDay.getTime() + 6 * 60 * 60 * 1000; // 6 AM
      newMaxTime = startOfDay.getTime() + 12 * 60 * 60 * 1000; // 12 PM
    } else if (selectedTimeSpan === 'afternoon_shift') {
      newMinTime = startOfDay.getTime() + 12 * 60 * 60 * 1000; // 12 PM
      newMaxTime = startOfDay.getTime() + 18 * 60 * 60 * 1000; // 6 PM
    } else if (selectedTimeSpan === 'last_30_min') {
      newMaxTime = Date.now();
      newMinTime = newMaxTime - 30 * 60 * 1000; // Last 30 minutes
    } else if (selectedTimeSpan === 'last_1_hour') {
      newMaxTime = Date.now();
      newMinTime = newMaxTime - 60 * 60 * 1000; // Last 1 hour
    } else if (selectedTimeSpan === 'last_10_min') {
      newMaxTime = Date.now();
      newMinTime = newMaxTime - 10 * 60 * 1000; // Last 10 minutes
    } else if (selectedTimeSpan === 'last_5_min') {
      newMaxTime = Date.now();
      newMinTime = newMaxTime - 5 * 60 * 1000; // Last 5 minutes
    }

    setMinTime(newMinTime);
    setMaxTime(newMaxTime);
    setTimeRange([newMinTime, newMaxTime]);
  }, [selectedDate, selectedTimeSpan]);

  const filteredRoutes = historicRoutes.filter(
    item => item.timestamp >= timeRange[0] && item.timestamp <= timeRange[1]
  );

  const handleTimeRangeChange = (range) => {
    setTimeRange(range);
  };

  const sortedRoute = filteredRoutes.sort((a, b) => a.timestamp - b.timestamp);
  const polylinePositions = sortedRoute.map(item => [item.latitude, item.longitude]);

  return (
    <div className="historic-routes-view">
      <h2>Historic Worker Routes</h2>

      <div className="controls-container">
        <div className="date-picker-container">
          <label>Select Date:</label>
          <DatePicker 
            selected={selectedDate}
            onChange={(date) => setSelectedDate(date)}
            dateFormat="MM/dd/yyyy"
            withPortal
          />
        </div>

        <div className="person-select-container">
          <label>Select Person:</label>
          <select
            value={selectedPerson || ''}
            onChange={(e) => setSelectedPerson(e.target.value)}
          >
            {people.map(person => (
              <option key={person.id} value={person.id}>
                {person.name}
              </option>
            ))}
          </select>
        </div>

        <div className="time-span-container">
          <label>Select Time Span:</label>
          <select value={selectedTimeSpan} onChange={(e) => setSelectedTimeSpan(e.target.value)}>
            <option value="full_day">Full Day</option>
            <option value="morning_shift">Morning Shift (6 AM - 12 PM)</option>
            <option value="afternoon_shift">Afternoon Shift (12 PM - 6 PM)</option>
            <option value="last_1_hour">Last 1 Hour</option>
            <option value="last_30_min">Last 30 Minutes</option>
            <option value="last_10_min">Last 10 Minutes</option>
            <option value="last_5_min">Last 5 Minutes</option>
          </select>
        </div>
      </div>

      {loading ? (
        <p>Loading historic routes...</p>
      ) : (
        <>
          {minTime && maxTime && (
            <div className="time-slider">
              <Slider
                range
                min={minTime}
                max={maxTime}
                step={1 * 60 * 1000} // 1-minute steps for better usability
                value={timeRange}
                onChange={handleTimeRangeChange}
                tipFormatter={(value) => new Date(value).toLocaleTimeString()}
              />
              <div className="time-range-labels">
                <span>{new Date(timeRange[0]).toLocaleTimeString()}</span>
                <span>{new Date(timeRange[1]).toLocaleTimeString()}</span>
              </div>
            </div>
          )}

          <MapContainer center={[53.375756, -6.523068]} zoom={16} className="map-container">
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution="&copy; OpenStreetMap contributors"
            />
            {polylinePositions.length > 0 && (
              <Polyline positions={polylinePositions} color="blue" />
            )}
          </MapContainer>
        </>
      )}
    </div>
  );
};

export default HistoricRoutesView;
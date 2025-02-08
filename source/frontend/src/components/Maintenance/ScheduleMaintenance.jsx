import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import './ScheduleMaintenance.css';

const ScheduleMaintenance = ({ buildings, workers, onSubmit }) => {
  const [selectedBuilding, setSelectedBuilding] = useState('');
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const [exemptWorkers, setExemptWorkers] = useState([]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      buildingId: selectedBuilding,
      start: startDate.toISOString(),
      end: endDate.toISOString(),
      exemptPersonnel: exemptWorkers
    });
  };

  return (
    <div className="schedule-form">
      <h3>Schedule Maintenance</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Building:</label>
          <select 
            value={selectedBuilding} 
            onChange={(e) => setSelectedBuilding(e.target.value)}
            required
          >
            <option value="">Select Building</option>
            {buildings.map(building => (
              <option key={building.id} value={building.id}>
                {building.name}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Start Date/Time:</label>
          <DatePicker
            selected={startDate}
            onChange={date => setStartDate(date)}
            showTimeSelect
            dateFormat="Pp"
          />
        </div>

        <div className="form-group">
          <label>End Date/Time:</label>
          <DatePicker
            selected={endDate}
            onChange={date => setEndDate(date)}
            showTimeSelect
            dateFormat="Pp"
            minDate={startDate}
          />
        </div>

        <div className="form-group">
          <label>Exempt Personnel:</label>
          <select 
            multiple
            value={exemptWorkers}
            onChange={(e) => setExemptWorkers([...e.target.selectedOptions].map(o => o.value))}
          >
            {workers.map(worker => (
              <option key={worker.id} value={worker.id}>
                {worker.name}
              </option>
            ))}
          </select>
        </div>

        <button type="submit">Schedule Maintenance</button>
      </form>
    </div>
  );
};

export default ScheduleMaintenance;
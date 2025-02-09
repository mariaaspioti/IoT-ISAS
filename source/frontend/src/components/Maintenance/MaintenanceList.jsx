import React from 'react';
import PropTypes from 'prop-types';
import './MaintenanceList.css';

const MaintenanceList = ({ maintenanceSchedules }) => {
  return (
    <div className="maintenance-list">
      <h3>Scheduled Maintenance</h3>
      <div className="maintenance-items">
        {maintenanceSchedules.map(schedule => (
          <div key={schedule.id} className="maintenance-item">
            <div className="maintenance-header">
              <span className="facility-id">{schedule.facilityName}</span>
              <span className={`status ${schedule.status.toLowerCase()}`}>
                {schedule.status}
              </span>
            </div>
            <div className="maintenance-details">
              <p><strong>Start:</strong> {new Date(schedule.startTime).toLocaleString()}</p>
              <p><strong>End:</strong> {new Date(schedule.endTime).toLocaleString()}</p>
              <p><strong>Description:</strong> {schedule.description}</p>
              <p><strong>Exempt Personnel:</strong></p>
              <ul>
                {/* {schedule?.peopleIds.map(personId => (
                  <li key={personId}>{personId}</li>
                ))} */}
                {schedule.peopleNames && schedule.peopleNames.length > 0 ? (
                    schedule.peopleNames.map(personName => (
                        <li key={personName}>{personName}</li>
                    ))
                ) : (
                    <li>None</li>
                )}
              </ul>
            </div>
          </div>
        ))}
        {maintenanceSchedules.length === 0 && (
          <div className="no-maintenance">
            No scheduled maintenance
          </div>
        )}
      </div>
    </div>
  );
};

MaintenanceList.propTypes = {
  maintenanceSchedules: PropTypes.array.isRequired
};

export default MaintenanceList;
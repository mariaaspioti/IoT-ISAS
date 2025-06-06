import React from 'react';
import PropTypes from 'prop-types';
import './AlertsList.css';

const AlertsList = ({ alerts, onDismissAlert, onUnlockDoors, onActivateAlarm }) => {

  const handleAction = (alertId, action) => {
    if (action === 'dismiss') {
      onDismissAlert(alertId);
    }
    else if (action === 'unlock') {
      // console.log(`Unlocking doors for alert ${alertId}`);
      onUnlockDoors(alertId);
    }
    else if (action === 'alarm') {
      console.log(`Activating alarm for alert ${alertId}`);
      onActivateAlarm(alertId);
    }
    else {
      console.log('Invalid action');
    }
  };

  return (
  <div className="alerts-container">
    <h3>Active Alerts ({alerts.length})</h3>
    <div className="alerts-list">
      {alerts.map(alert => (
        <div key={alert.id} className="alert-item">
          <div className="alert-header">
            <span className="alert-id">Alert #{alert.id}</span>
            {/* <span className="alert-time">{alert.dateIssued.value}</span> */}
            <span className="alert-time">{alert.dateIssued}</span>
          </div>
          <div className="alert-body">
            <span className="alert-severity">{alert.severity}</span>
            <p className="alert-description">{alert.description}</p>
            <div className="alert-meta">
                  <span className="alert-person">Owner: {alert.personName}</span>
                  <span className="alert-location">
                    
                    {alert.personCurrentFacility && (
                      <>
                        <span>Current Facility:</span> {alert.personCurrentFacility}<br />
                      </>
                    )}
                    {alert.personCurrentLocation && (
                      <>
                      <span>Current Location:</span> {alert.personCurrentLocation.join(', ')}
                      </>
                    )}
                    </span>
                  <span className="alert-status">Status: {alert.status}</span>
                </div>
          </div>
          <div className="alert-actions">
                <select
                  disabled={alert.status === 'resolved'}
                  className="action-select"
                  onChange={(e) => {
                    handleAction(alert.id, e.target.value);
                    e.target.value = ''; // Reset selection
                  }}
                >
                  {alert.status === 'resolved' && (
                    <option value="">Resolved</option>
                  )}
                  <option value="">Actions...</option>
                  <option value="unlock" disabled={alert.personCurrentFacility === "Outside"}>Unlock Doors</option>
                  <option value="alarm">Activate Alarm</option>
                  <option value="dismiss">Dismiss</option>
                </select>
              </div>
        </div>
      ))}
      {alerts.length === 0 && (
        <div className="no-alerts">No active alerts</div>
      )}
    </div>
  </div>
);
};

AlertsList.propTypes = {
  alerts: PropTypes.array.isRequired,
  onDismissAlert: PropTypes.func.isRequired
};

export default AlertsList;
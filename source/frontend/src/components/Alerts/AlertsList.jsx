import React from 'react';
import PropTypes from 'prop-types';
import './AlertsList.css';

const AlertsList = ({ alerts }) => (
  <div className="alerts-container">
    <h3>Active Alerts ({alerts.length})</h3>
    <div className="alerts-list">
      {alerts.map(alert => (
        <div key={alert.id} className="alert-item">
          <div className="alert-header">
            <span className="alert-id">Alert #{alert.id}</span>
            {/* <span className="alert-time">{alert.dateIssued.value}</span> */}
            <span className="alert-time">{alert.frontend_timestamp}</span>
          </div>
          <div className="alert-body">
            <span className="alert-severity">{alert.severity.value}</span>
            <p className="alert-description">{alert.description.value}</p>
          </div>
        </div>
      ))}
      {alerts.length === 0 && (
        <div className="no-alerts">No active alerts</div>
      )}
    </div>
  </div>
);

AlertsList.propTypes = {
  alerts: PropTypes.array.isRequired
};

export default AlertsList;
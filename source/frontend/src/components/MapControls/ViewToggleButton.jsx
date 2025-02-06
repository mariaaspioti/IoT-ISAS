import React from 'react';
import PropTypes from 'prop-types';

const ViewToggleButton = ({ viewType, activeView, children, onClick }) => {
  const buttonStyle = {
    margin: '0 10px',
    padding: '10px 20px',
    backgroundColor: activeView === viewType ? '#007bff' : '#6c757d',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    transition: 'background-color 0.3s'
  };

  return (
    <button 
      style={buttonStyle}
      onClick={() => onClick(viewType)}
    >
      {children}
    </button>
  );
};

ViewToggleButton.propTypes = {
  viewType: PropTypes.string.isRequired,
  activeView: PropTypes.string.isRequired,
  children: PropTypes.node.isRequired,
  onClick: PropTypes.func.isRequired
};

export default ViewToggleButton;
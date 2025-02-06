import React from 'react';
import PropTypes from 'prop-types';
import ViewToggleButton from './ViewToggleButton';
import { VIEW_TYPES } from '../../constants';

const ViewControls = ({ activeView, setActiveView }) => (
  <div className="controls">
    <ViewToggleButton 
      viewType={VIEW_TYPES.BUILDINGS}
      activeView={activeView}
      onClick={setActiveView}
    >
      Show Buildings
    </ViewToggleButton>
    <ViewToggleButton
      viewType={VIEW_TYPES.DOORS}
      activeView={activeView}
      onClick={setActiveView}
    >
      Show Doors
    </ViewToggleButton>
    <ViewToggleButton
      viewType={VIEW_TYPES.PEOPLE}
      activeView={activeView}
      onClick={setActiveView}
    >
      Show People
    </ViewToggleButton>
  </div>
);

ViewControls.propTypes = {
  activeView: PropTypes.string.isRequired,
  setActiveView: PropTypes.func.isRequired
};

export default ViewControls;
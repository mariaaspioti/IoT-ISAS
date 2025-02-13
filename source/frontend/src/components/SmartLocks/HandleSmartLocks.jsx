import React, { useState, useEffect } from 'react';
import Select from 'react-select';
import { fetchAllSmartLocks, patchSmartLockAction } from '../../services/api';
import './HandleSmartLocks.css';

const HandleSmartLocks = ({ onSubmit }) => {
  const [smartLocks, setSmartLocks] = useState([]);
  const [selectedSmartLock, setSelectedSmartLock] = useState(null);
  const [selectedAction, setSelectedAction] = useState(null);
  const [actionOptions, setActionOptions] = useState([]);
  const [deviceState, setDeviceState] = useState('');
  const [hardLock, setHardLock] = useState(false);

  useEffect(() => {
    const fetchSmartLocks = async () => {
      try {
        const data = await fetchAllSmartLocks();
        setSmartLocks(data);
      } catch (error) {
        console.error('Error fetching smart locks:', error);
      }
    };

    fetchSmartLocks();
  }, []);

  const smartLockOptions = smartLocks.map(lock => ({
    value: lock.id,
    label: `${lock.name.value} (ID: ${lock.id}), ${lock.areaServed.value}`,
    hardLock: lock.hardLock.value,
    deviceState: lock.deviceState.value,
  }));

  const updateActionOptions = (selectedLock) => {
    if (!selectedLock) {
      setActionOptions([]);
      return;
    }

    const options = [
      { value: 'unlock', label: 'Unlock', isDisabled: selectedLock.deviceState === 'unlocked' || selectedLock.hardLock },
      { value: 'lock', label: 'Lock', isDisabled: selectedLock.deviceState === 'locked' },
      { value: 'disableUnlocking', label: 'Disable Unlocking', isDisabled: selectedLock.deviceState === 'unlocked' || selectedLock.hardLock },
      { value: 'enableUnlocking', label: 'Enable Unlocking', isDisabled: !selectedLock.hardLock },
    ];

    setActionOptions(options);
  };

  const handleSmartLockChange = (option) => {
    if (!option) {
      setSelectedSmartLock(null);
      setDeviceState('');
      setHardLock(false);
      setActionOptions([]);
      return;
    }

    setSelectedSmartLock(option);
    setDeviceState(option.deviceState);
    setHardLock(option.hardLock);
    updateActionOptions(option);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await patchSmartLockAction(selectedSmartLock.value, selectedAction.value);
      onSubmit({
        smartLockId: selectedSmartLock.value,
        action: selectedAction.value,
      });

      // Reset form fields to initial state
      setSelectedSmartLock(null);
      setSelectedAction(null);
      setActionOptions([]);
      setDeviceState('');
      setHardLock(false);

      // Fetch the smart locks again after the action is completed
      const updatedSmartLocks = await fetchAllSmartLocks();
      setSmartLocks(updatedSmartLocks); // Update state with the fresh data

    } catch (error) {
      console.error('Error submitting smart lock action:', error);
    }
  };

  return (
    <div className="handle-smart-locks-form">
      <h3>Handle Smart Locks</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Smart Lock:</label>
          <Select
            value={selectedSmartLock}
            onChange={handleSmartLockChange}
            options={smartLockOptions}
            placeholder="Select Smart Lock..."
            className="smart-lock-select"
            isClearable
          />
        </div>

        {selectedSmartLock && (
          <div className="form-group">
            <label>
              {hardLock ? 'Unlocking is Disabled' : `Device State: ${deviceState}`}
            </label>
          </div>
        )}

        <div className="form-group">
          <label>Action:</label>
          <Select
            value={selectedAction}
            onChange={(option) => setSelectedAction(option)}
            options={actionOptions}
            placeholder="Select Action..."
            className="action-select"
            isOptionDisabled={(option) => option.isDisabled}
            isClearable
          />
        </div>

        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default HandleSmartLocks;
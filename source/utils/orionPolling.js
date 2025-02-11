import axios from 'axios';
import fs from 'fs';
import path from 'path';
import { handleNFCDeviceUpdates } from '../controllers/accessController.mjs';

// Orion Context Broker URL
const orionUrl = 'http://150.140.186.118:1026/v2/entities';
const fiwareService = 'ISAS';
const fiwareServicePath = '/test';
const getHeaders = {
    'Fiware-Service': fiwareService,
    'Fiware-ServicePath': fiwareServicePath,
};

const logDir = './logs';
const logFile = path.join(logDir, 'alertData.log');
if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir);
}

// A set to store processed alerts by ID
let processedAlerts = new Set();

/**
 * Starts polling Orion for alert data and emits new alerts via the provided socket.
 *
 * @param {object} socket - The Socket.IO instance used for emitting events.
 * @param {number} intervalMs - Polling interval in milliseconds (default is 2000 ms).
 * @returns {Function} - A function to stop the polling.
 */
export const startAlertPolling = (socket, intervalMs = 2000) => {
  const fetchAlertData = async () => {
    try {
      const queryParams = { 
        headers: getHeaders,
        params: {
          type: 'Alert',
          q: 'category==security;subCategory==suspiciousAction',
        },
      };

      const response = await axios.get(orionUrl, queryParams);
      const alertData = response.data;

      if (!alertData.length) {
        return;
      }

      // Iterate over each alert and emit if it hasn't been processed before
      alertData.forEach((alert) => {
        if (!processedAlerts.has(alert.id)) {
          processedAlerts.add(alert.id);
          socket.emit('alertSOSbutton', alert);
          console.log('Emitted new alert:', alert);

          // Log the new alert data to a file
          fs.appendFile(logFile, JSON.stringify(alert, null, 2) + "\n", (err) => {
            if (err) {
              console.error('Error writing alert data to file:', err);
            }
          });
        }
      });
    } catch (error) {
      console.error('Error fetching alert data:', error.message);
    }
  };

  // Start polling at the specified interval
  const interval = setInterval(fetchAlertData, intervalMs);
  return () => clearInterval(interval);
};


// A map to store the previous state of NFC devices by ID
let previousState = new Map();


/**
 * Starts polling Orion for NFC device data and emits new data via the provided socket.
 *
 * @param {object} socket - The Socket.IO instance used for emitting events.
 * @param {number} intervalMs - Polling interval in milliseconds (default is 2000 ms).
 * @returns {Function} - A function to stop the polling.
 */
export const startNFCPolling = (socket, intervalMs = 2000, limit = 100) => { 
  let isFirstPoll = true;

  const fetchNFCData = async () => {
    try {
      const queryParams = {
        headers: getHeaders,
        params: {
          type: 'Device',
          q: "name~=^NFCReader-", // query to match names starting with NFCReader-
          limit: limit, // Set the limit parameter
        },
      };

      const response = await axios.get(orionUrl, queryParams);
      const deviceData = response.data;

      if (!deviceData.length) {
        return;
      }

      // // Iterate over each device and check for changes
      // deviceData.forEach((device) => {
      //   const currentValue = device.value.value;
      //   const currentDateLastValueReported = device.dateLastValueReported.value;

      //   if (isFirstPoll) {
      //     // Save the current state as the previous state during the first poll
      //     previousState.set(device.id, {
      //       value: currentValue,
      //       dateLastValueReported: currentDateLastValueReported
      //     });
      //   } else {
      //     const previousDevice = previousState.get(device.id);

      //     if (!previousDevice || 
      //         previousDevice.value !== currentValue || 
      //         previousDevice.dateLastValueReported !== currentDateLastValueReported) {
      //       previousState.set(device.id, {
      //         value: currentValue,
      //         dateLastValueReported: currentDateLastValueReported
      //       });
      //       // console.log('Device state changed:', device);

      //       // Forward the data to the controller for processing
      //       const result = await handleNFCDeviceUpdates(device, socket);

      //       // Emit the change via Socket.IO
      //       socket.emit('nfcDeviceUpdate', device, result);
      //     }
      //   }
      // });
      for (const device of deviceData) {
        const currentValue = device.value.value;
        const currentDateLastValueReported = device.dateLastValueReported.value;
  
        if (isFirstPoll) {
          // Save the current state as the previous state during the first poll
          previousState.set(device.id, {
            value: currentValue,
            dateLastValueReported: currentDateLastValueReported,
          });
        } else {
          const previousDevice = previousState.get(device.id);
  
          if (
            !previousDevice ||
            previousDevice.value !== currentValue ||
            previousDevice.dateLastValueReported !== currentDateLastValueReported
          ) {
            previousState.set(device.id, {
              value: currentValue,
              dateLastValueReported: currentDateLastValueReported,
            });
            // Forward the data to the controller for processing
            const result = await handleNFCDeviceUpdates(device, socket);
            // Emit the change via Socket.IO
            socket.emit('nfcDeviceUpdate', device, result);
          }
        }
      }

      // Set isFirstPoll to false after the first poll
      isFirstPoll = false;
    } catch (error) {
      console.error('Error fetching NFC device data:', error.message);
    }
  };

  // Start polling at the specified interval
  const interval = setInterval(fetchNFCData, intervalMs);
  return () => clearInterval(interval);
};
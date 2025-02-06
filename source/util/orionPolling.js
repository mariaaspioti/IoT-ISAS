import axios from 'axios';
import fs from 'fs';

// Orion Context Broker URL
const orionUrl = 'http://150.140.186.118:1026/v2/entities';
const fiwareService = 'ISAS';
const fiwareServicePath = '/test';
const getHeaders = {
    'Fiware-Service': fiwareService,
    'Fiware-ServicePath': fiwareServicePath,
};

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
      // Log the alert data to a file
      fs.appendFile(
        './logs/alertData.log',
        JSON.stringify(alertData, null, 2) + "\n",
        (err) => {
          if (err) {
            console.error('Error writing alert data to file:', err);
          }
        }
      );

      // Iterate over each alert and emit if it hasn't been processed before
      alertData.forEach((alert) => {
        if (!processedAlerts.has(alert.id)) {
          processedAlerts.add(alert.id);
          socket.emit('alertSOSbutton', alert);
          console.log('Emitted new alert:', alert);
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
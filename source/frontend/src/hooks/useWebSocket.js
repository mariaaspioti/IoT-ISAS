import { useEffect, useCallback } from 'react';
import io from 'socket.io-client';
import { SOCKET_SERVER_URL } from '../constants';

const useWebSocket = (eventHandlers) => {
  const connectSocket = useCallback(() => {
    const socket = io(SOCKET_SERVER_URL);

    socket.on('connect', () => {
      console.log('Connected to Socket.IO server');
    });

    // Set up all event handlers
    Object.entries(eventHandlers).forEach(([eventName, handler]) => {
      socket.on(eventName, handler);
    });

    socket.on('disconnect', () => {
      console.log('Disconnected from Socket.IO server');
    });

    return socket;
  }, [eventHandlers]); // Reconnect if handlers change

  useEffect(() => {
    const socket = connectSocket();
    return () => socket.disconnect();
  }, [connectSocket]);
};

export default useWebSocket;
import { useEffect, useCallback } from 'react';
import io from 'socket.io-client';
import { SOCKET_SERVER_URL } from '../constants';

const useWebSocket = (handleNewAlert) => {
  const connectSocket = useCallback(() => {
    const socket = io(SOCKET_SERVER_URL);

    socket.on('connect', () => {
      console.log('Connected to Socket.IO server');
    });

    socket.on('alertSOSbutton', handleNewAlert);

    socket.on('disconnect', () => {
      console.log('Disconnected from Socket.IO server');
    });

    return socket;
  }, [handleNewAlert]);

  useEffect(() => {
    const socket = connectSocket();
    return () => socket.disconnect();
  }, [connectSocket]);
};

export default useWebSocket;
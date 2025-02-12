import { useEffect, useCallback, useRef } from 'react';
import io from 'socket.io-client';
import { SOCKET_SERVER_URL } from '../constants';

const useWebSocket = (eventHandlers) => {
  const socketRef = useRef(null);
  const handlersRef = useRef(eventHandlers);

  // Keep handlersRef updated without causing re-renders
  useEffect(() => {
    handlersRef.current = eventHandlers;
  }, [eventHandlers]);

  useEffect(() => {
    // Singleton socket instance
    if (!socketRef.current) {
      socketRef.current = io(SOCKET_SERVER_URL, {
        withCredentials: true,
        transports: ['websocket', 'polling'],
        reconnectionAttempts: 5,
        autoConnect: true,
        closeOnBeforeunload: false
      });

      const socket = socketRef.current;

      socket.on('connect', () => {
        console.log('Connected to Socket.IO server');
      });

      socket.on('disconnect', (reason) => {
        console.log('Disconnected:', reason);
      });

      socket.on('connect_error', (err) => {
        console.log('Connection error:', err.message);
      });
    }

    const socket = socketRef.current;

    // Event listener setup
    const currentHandlers = handlersRef.current;
    Object.entries(currentHandlers).forEach(([event, handler]) => {
      socket.off(event); // Remove old listeners
      socket.on(event, handler);
    });

    // Cleanup only on unmount
    return () => {
      if (socketRef.current) {
        socketRef.current.off();
        socketRef.current.disconnect();
        socketRef.current = null;
      }
    };
  }, []);

  // Handle reconnect on network recovery
  const handleVisibilityChange = useCallback(() => {
    if (document.visibilityState === 'visible' && socketRef.current?.disconnected) {
      socketRef.current.connect();
    }
  }, []);

  useEffect(() => {
    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  }, [handleVisibilityChange]);
};

export default useWebSocket;
import { useState, useCallback, useEffect } from 'react';
import * as editMap from '../services/editMap';
import { VIEW_TYPES } from '../constants';

const useMapData = () => {
  const [loading, setLoading] = useState(true);
  const [mapData, setMapData] = useState({
    [VIEW_TYPES.BUILDINGS]: [],
    [VIEW_TYPES.DOORS]: [],
    [VIEW_TYPES.PEOPLE]: []
  });

  const fetchData = useCallback(async () => {
    try {
      const { mapData } = await editMap.fetchTrackingData();
      const doors = await editMap.showDoors();
      const buildings = await editMap.showBuildings();
      
      setMapData(prev => ({
        [VIEW_TYPES.BUILDINGS]: buildings || prev[VIEW_TYPES.BUILDINGS],
        [VIEW_TYPES.DOORS]: doors || prev[VIEW_TYPES.DOORS],
        [VIEW_TYPES.PEOPLE]: mapData || prev[VIEW_TYPES.PEOPLE]
      }));
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, [fetchData]);

  return { loading, mapData };
};

export default useMapData;
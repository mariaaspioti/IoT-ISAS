import { useState, useCallback, useEffect } from 'react';
import * as editMap from '../services/editDashboardData';
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
      const { mapData: peopleRaw } = await editMap.fetchTrackingData();
      // const doors = await editMap.showDoors();
      const doors = await editMap.fetchAllSmartLocksData();
      const buildings = await editMap.showBuildings();

      // Deduplicate PEOPLE data using a Map object (keeps latest entry per id)
      // console.log("peopleRaw:", peopleRaw);
      const latestPeople = Object.values(
        peopleRaw.reduce((acc, person) => {
          acc[person.person_id] = person; // Override previous entry with the same ID
          return acc;
        }, {})
      );
      
      setMapData(prev => ({
        [VIEW_TYPES.BUILDINGS]: buildings || prev[VIEW_TYPES.BUILDINGS],
        [VIEW_TYPES.DOORS]: doors || prev[VIEW_TYPES.DOORS],
        [VIEW_TYPES.PEOPLE]: latestPeople || prev[VIEW_TYPES.PEOPLE]
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
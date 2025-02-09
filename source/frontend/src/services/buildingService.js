const coordinateCache = new Map();

export const fetchBuildingCoordinates = async (buildingId) => {
  if (coordinateCache.has(buildingId)) {
    return coordinateCache.get(buildingId);
  }

  try {
    const response = await fetch(`/api/facilities/${buildingId}/location`);
    console.log("Building id: ", buildingId, "and response: ", response);
    if (!response.ok) throw new Error('Failed to fetch coordinates');
    const coordinates = await response.json();
    coordinateCache.set(buildingId, coordinates);
    return coordinates;
  } catch (error) {
    console.error(`Error fetching coordinates for building ${buildingId}:`, error);
    throw error;
  }
};
// import turf
import * as turf from '@turf/turf';
import axios from 'axios';
// Orion Context Broker URL
const orionUrl = 'http://150.140.186.118:1026/v2/entities';
const fiwareService = 'ISAS';
const fiwareServicePath = '/test';
const getHeaders = {
    'Fiware-Service': fiwareService,
    'Fiware-ServicePath': fiwareServicePath,
};
const postPatchHeaders = {
    'Content-Type': 'application/json',
    'Fiware-Service': fiwareService,
    'Fiware-ServicePath': fiwareServicePath,
};

// ============== Functions for state management ==============

// This function will update the currentFacility attribute of the persons
// given the input of { lat: number, lng: number, facility_id: string, facility_name: string }
// for each person in the normal order of the persons array
export const updateCurrentFacilityForPersons = async (personsFacilityData) => {
    try {
        // get all persons from the Orion Context Broker
        const response = await axios.get(orionUrl + '/?type=Person', { headers: getHeaders });
        const persons = response.data;

        // for each person, update the currentFacility attribute
        for (let i = 0; i < persons.length; i++) {
            // skip the iteration, if the person 
            // does not have a facility_id in the personsFacilityData
            if (!personsFacilityData[i]?.facility_id) continue;
            const person = persons[i];
            const facilityData = personsFacilityData[i];
            const personData = {
                currentFacility: {
                    type: 'Relationship',
                    value: facilityData.facility_id,
                },
            };
            const personUrl = `${orionUrl}/${person.id}/attrs`;
            await axios.post(personUrl, personData, { headers: postPatchHeaders });
        }
    } catch (error) {
        console.error('Error updating currentFacility for persons:', error);
        throw error;
    }
};      

// ============== Functions for processing facilities ==============
export const arraysEqual = (a, b) => {
  return a.length === b.length && a.every((val, i) => val === b[i]);
};

const validateFacility = (facility) => {
  if (!facility.bounds || facility.bounds.length < 3) {
    console.warn(`Invalid facility ${facility.id}`);
    return false;
  }
  return true;
};

const createValidPolygon = (coords) => {
  const formatted = coords.map(coord => [coord[0], coord[1]]);
  if (!arraysEqual(formatted[0], formatted[formatted.length-1])) {
    formatted.push(formatted[0]);
  }
  return turf.polygon([formatted]);
};

export const findFacilityContainingPoint = (point, facilities) => {
  try {
    return facilities.find(f => {
      if (!validateFacility(f)) return false;
      const polygon = createValidPolygon(f.bounds);
      return turf.booleanPointInPolygon(point, polygon);
    });
  } catch (error) {
    console.error('Geospatial error:', error);
    return null;
  }
};

// This function finds the facility that contains the given points
// and returns an array of objects with the following structure:
// { lat: number, lng: number, facility: { id: string, name: string } }
// The facility object is null if the point is not within any facility
export const processFacilities = async (coordinates, rawFacilities) => {
  const facilities = rawFacilities.map(f => ({
    id: f.id,
    name: f.name.value,
    bounds: f.location.value.coordinates[0]
  }));

  return Promise.all(coordinates.map(loc => {
    const point = turf.point([loc.lng, loc.lat]);
    const facility = findFacilityContainingPoint(point, facilities);
    return {
      lat: loc.lat,
      lng: loc.lng,
      ...(facility ? { id: facility.id, name: facility.name } : {})

    };
  }));
};
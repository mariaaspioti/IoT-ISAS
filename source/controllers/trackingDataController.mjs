import * as influxInterface from '../model/influxInterface.mjs';
import { Point } from '@influxdata/influxdb-client';

export const connectToDatabase = () => {
    influxInterface.connectToInfluxDB();
}

//
// export const writeNewPoint = async (measurement, tags, floatFields, stringFields) => {
//     await influxInterface.writeNewPoint(influxInterface.connectToInfluxDB(), measurement, tags, floatFields, stringFields);
// }


export const writeWorkerTrackingData = async (trackingDataArray) => {
    // Expecting an array of objects with the following structure:
    // [{
    //     lat: number,
    //     lng: number,
    //     facility_name: string,
    //     facility_id: string,
    //     person_id: string
    //     person_name: string
    //     person_role: string
    // },
    // ...

    // console.log("trackingData in writeWorkerTrackingData:", trackingData);
    if (!Array.isArray(trackingDataArray) || trackingDataArray.length === 0) {
        console.error("Invalid tracking data: Expected a non-empty array.");
        return;
    }

    const measurement = 'worker_tracking';
    
    // Iterate over the array and prepare points
    const points = trackingDataArray.map(trackingData => {
        const point = new Point(measurement)
            .tag("facility_id", trackingData.facility_id)
            .tag("person_id", trackingData.person_id)
            .tag("person_role", trackingData.person_role)
            .floatField("lat", trackingData.lat)
            .floatField("lng", trackingData.lng)
            .stringField("facility_name", trackingData.facility_name)
            .stringField("person_name", trackingData.person_name);

        return point;
    });

    // Write all points in bulk to InfluxDB
    try {
        await influxInterface.writeMultiplePoints(points);
        console.log(`Successfully wrote ${trackingDataArray.length} tracking data points.`);
    } catch (error) {
        console.error("Error writing tracking data:", error);
    }
}

export const fetchHistoricTrackingData = async (date, personId) => {
    const startTime = new Date(date);
    startTime.setHours(0, 0, 0, 0); // Set to start of the day

    const endTime = new Date(date);
    endTime.setHours(23, 59, 59, 999); // Set to end of the day

    const measurement = 'worker_tracking';
    const results = await influxInterface.readPointsForTimespan(measurement, startTime, endTime, personId);

    // Format results to match the expected structure in the frontend { person_id, facility_id, timestamp, latitude, longitude }
    const formattedResults = results
    .filter(result => result.lat && result.lng) // Filter out points with missing lat/lng
    .map(result => ({
        person_id: result.person_id,
        facility_id: result.facility_id,
        timestamp: result._time,
        latitude: result.lat,
        longitude: result.lng
    }));

    return formattedResults;
};

import { InfluxDB, Point } from "@influxdata/influxdb-client";
import dotenv from 'dotenv';

dotenv.config();

const url = process.env.INFLUX_URL || 'http://150.140.186.118:8086';
const bucket = process.env.INFLUX_BUCKET || 'ISAS';
const org = "students";
const token = process.env.INFLUX_TOKEN || "lcIckpaO0SHe25GY5q8QQVvZtZw0cEalVeSCfVk1WO20R1d8BEiYJJ1RQhxRJBnpn3uX3qJoumVB2k_OcRNbpQ=="
if (!token) {
    console.error('No token provided for InfluxDB');
    process.exit(1);
}

// export const connectToInflux = () => {
//     return new InfluxDB({ url, token });
// }
const db = new InfluxDB({ url, token });
const writeApi = db.getWriteApi(org, bucket, 's');

export const writeMultiplePoints = async (points) => {
    // const writeApi = db.getWriteApi(org, bucket, 's');

    writeApi.writePoints(points);

    await writeApi.flush()
        .then(() => console.log('BULK WRITE FINISHED'))
        .catch(e => { console.error('Error writing points:', e); });
};

// export const writeNewPoint = async (measurement, tags, floatFields, stringFields) => {
//     const point = new Point(measurement);

//     // Add tags
//     Object.keys(tags).forEach(key => {
//         point.tag(key, tags[key]);
//     });

//     // Add float fields
//     Object.keys(floatFields).forEach(key => {
//         point.floatField(key, floatFields[key]);
//     });

//     // Add string fields
//     Object.keys(stringFields).forEach(key => {
//         point.stringField(key, stringFields[key]);
//     });

//     writeApi.writePoint(point);
//     await writeApi.flush()
//       .then(() => console.log('WRITE FINISHED'))
//       .catch(e => { console.error(e) });
// }

// Function to read points for a given timespan and person ID
export const readPointsForTimespan = async (measurement, startTime, endTime, personId) => {
    const queryApi = db.getQueryApi(org);

    // Construct a Flux query with a filter for the specific person ID
    const fluxQuery = `
        from(bucket: "${bucket}")
            |> range(start: ${startTime.toISOString()}, stop: ${endTime.toISOString()})
            |> filter(fn: (r) => r._measurement == "${measurement}")
            |> filter(fn: (r) => r.person_id == "${personId}")
            |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
        `;

    return new Promise((resolve, reject) => {
        const results = [];
        queryApi.queryRows(fluxQuery, {
            next(row, tableMeta) {
                results.push(tableMeta.toObject(row));
            },
            error(error) {
                console.error('Query error:', error);
                reject(error);
            },
            complete() {
                resolve(results);
            }
        });
    });
};

// Initialize connection cleanup on process exit
process.on('SIGINT', async () => {
    try {
        await writeApi.close();
        console.log('InfluxDB connection closed');
    } catch (error) {
        console.error('Error closing InfluxDB connection:', error);
    }
    process.exit();
});
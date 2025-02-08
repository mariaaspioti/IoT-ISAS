import sqlite3 from 'sqlite3';
import path from 'path';
import { fileURLToPath } from 'url';
import * as sqlCode from './SQL/statements.mjs';

// Convert import.meta.url to a file path
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const dbPath = path.resolve(__dirname, '../database/ISAS_database.db');

export const connectToDatabase = () => {
    const db = new sqlite3.Database(dbPath, (err) => {
        if (err) {
            console.error('Error connecting to database:', err);
        } else {
            console.log('Connected to database');
        }
    });
    return db;
};

export const insertMaintenanceRecord = (record, callback) => {
    const { startTime, endTime, dateCreated, status, description, peopleIds, facilityId } = record;
    // Maintenance record --> startTime, endTime, dateCreated, status, description
    // Person conducts maintenance --> personId, maintenanceId
    // Maintenance reserves facility --> facilityId, maintenanceId

    const db = connectToDatabase();

    db.serialize(() => {
        db.run(sqlCode.insertMaintenance, [startTime, endTime, dateCreated, status, description], function (err) {
            if (err) {
                console.error('Error inserting maintenance record:', err);
            } else {
                const maintenanceId = this.lastID;
                peopleIds.forEach(personId => {
                    db.run(sqlCode.insertPersonConductsMaintenance, [personId, maintenanceId], function (err) {
                        if (err) {
                            console.error('Error inserting person conducts maintenance:', err);
                        }
                    });
                });
                db.run(sqlCode.insertMaintenanceReservesFacility, [facilityId, maintenanceId], function (err) {
                    if (err) {
                        console.error('Error inserting maintenance reserves facility:', err);
                    }
                    callback(null); // No error
                });
            }
        });
    });
    return record;
};

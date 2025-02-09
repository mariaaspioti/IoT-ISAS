import sqlite3 from 'sqlite3';
import path from 'path';
import { fileURLToPath } from 'url';
import * as sqlCode from './SQL/statements.mjs';
import e from 'express';

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

export const getFacilityById = (facilityId) => {
    const db = connectToDatabase();
    return new Promise((resolve, reject) => {
        db.get(sqlCode.selectFacilityById, [facilityId], (err, row) => {
            if (err) {
                console.error('Error fetching facility:', err);
                reject(err);
            } else {
                resolve(row);
            }
        });
    });
};

export const getFacilityByCBId = (facilityId) => {
    const db = connectToDatabase();
    return new Promise((resolve, reject) => {
        db.get(sqlCode.selectFacilityByCBId, [facilityId], (err, row) => {
            if (err) {
                console.error('Error fetching facility:', err);
                reject(err);
            } else {
                resolve(row);
            }
        });
    });
};

export const getPersonById = (personId) => {
    const db = connectToDatabase();
    return new Promise((resolve, reject) => {
        db.get(sqlCode.selectPersonById, [personId], (err, row) => {
            if (err) {
                console.error('Error fetching person:', err);
                reject(err);
            } else {
                resolve(row);
            }
        });
    });
};

export const getPersonByCBId = (personId) => {
    const db = connectToDatabase();
    return new Promise((resolve, reject) => {
        db.get(sqlCode.selectPersonByCBId, [personId], (err, row) => {
            if (err) {
                console.error('Error fetching person:', err);
                reject(err);
            } else {
                resolve(row);
            }
        });
    });
};

export const insertMaintenanceRecord = (record, callback) => {
    const { startTime, endTime, dateCreated, status, description, peopleIds, facilityId } = record;
    // Maintenance record --> startTime, endTime, dateCreated, status, description
    // Person conducts maintenance --> personId, maintenanceId
    // Maintenance reserves facility --> maintenanceId, facilityId

    const db = connectToDatabase();
    console.log('Inserting maintenance record in insertMaintenanceRecord:', record);
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
                db.run(sqlCode.insertMaintenanceReservesFacility, [maintenanceId, facilityId], function (err) {
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

export const getScheduledMaintenances = (callback) => {
    const db = connectToDatabase();

    db.all(sqlCode.selectScheduledMaintenances, (err, rows) => {
        if (err) {
            console.error('Error fetching scheduled maintenances:', err);
            return callback(err);
        }
        callback(null, rows);
    });
};
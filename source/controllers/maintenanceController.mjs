import * as dbInterface from '../model/dbInterface.mjs';

export const connectToDatabase = () => {
    dbInterface.connectToDatabase();
};

export const insertMaintenanceRecord = (maintenance, callback) => {
    dbInterface.insertMaintenanceRecord(maintenance, (err) => {
        if (err) {
            console.error('Error inserting maintenance record:', err);
            return callback(err);
        }
        callback(null); // Success
    });
};
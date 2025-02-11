import * as dbInterface from '../model/dbInterface.mjs';

export const connectToDatabase = () => {
    dbInterface.connectToDatabase();
};

export const getFacilityById = async (facilityId) => {
    try {
        const facility = await dbInterface.getFacilityById(facilityId);
        return facility;
    } catch (err) {
        console.error('Error fetching facility:', err);
        throw err;
    }
};

export const getFacilityByCBId = async (facilityId) => {
    try {
        const facility = await dbInterface.getFacilityByCBId(facilityId);
        return facility;
    } catch (err) {
        console.error('Error fetching facility:', err);
        throw err;
    }
};

export const getPersonById = async (personId) => {
    try {
        const person = await dbInterface.getPersonById(personId);
        return person;
    } catch (err) {
        console.error('Error fetching person:', err);
        throw err;
    }
}

export const getPersonByCBId = async (personId) => {
    try {
        const person = await dbInterface.getPersonByCBId(personId);
        return person;
    } catch (err) {
        console.error('Error fetching person:', err);
        throw err;
    }
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

export const getScheduledMaintenances = (callback) => {
    dbInterface.getScheduledMaintenances((err, maintenances) => {
        if (err) {
            console.error('Error fetching scheduled maintenances:', err);
            return callback(err);
        }
        callback(null, maintenances);
    });
};

export const updateMaintenanceStatus = (maintenanceId, status, callback) => {
    dbInterface.updateMaintenanceStatus(maintenanceId, status, (err) => {
        if (err) {
            console.error('Error updating maintenance status:', err);
            return callback(err);
        }
        callback(null); // Success
    });
};
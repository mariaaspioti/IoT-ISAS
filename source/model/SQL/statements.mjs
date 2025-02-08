export const insertMaintenance = `
    INSERT INTO Maintenance (startTime, endTime, dateCreated, status, description)
    VALUES (?, ?, ?, ?, ?);
    `;


export const insertPersonConductsMaintenance = `
    INSERT INTO Conducts (person_id, maintenance_id)
    VALUES (?, ?);
    `;

export const insertMaintenanceReservesFacility = `
    INSERT INTO Reserves (maintenance_id, facility_id)
    VALUES (?, ?);
    `;



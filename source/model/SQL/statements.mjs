export const selectFacilityById = `
    SELECT * FROM Facility WHERE facility_id = ?;
    `;

export const selectFacilityByCBId = `
    SELECT * FROM Facility WHERE context_broker_id = ?;
    `;

export const selectPersonById = `
    SELECT * FROM Person WHERE person_id = ?;
    `;

export const selectPersonByCBId = `
    SELECT * FROM Person WHERE context_broker_id = ?;
    `;


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

// select all maintenances that have startTime > now,
// and all person_ids that 'conducts' the maintenance
// and the facility_id that 'reserves' (is reserved by) the maintenance
export const selectScheduledMaintenances = `
    SELECT 
        m.maintenance_id, 
        m.startTime, 
        m.endTime, 
        m.dateCreated, 
        m.status, 
        m.description, 
        GROUP_CONCAT(c.person_id) AS person_ids, 
        r.facility_id
    FROM Maintenance m
    LEFT JOIN Conducts c ON m.maintenance_id = c.maintenance_id
    LEFT JOIN Reserves r ON m.maintenance_id = r.maintenance_id
    WHERE datetime(m.startTime) > datetime('now') AND m.status = 'scheduled'
    GROUP BY m.maintenance_id, m.startTime, m.endTime, m.dateCreated, m.status, m.description
    ORDER BY m.startTime;
    `;

// given the maintenance id and the new status, update the status of the maintenance
export const updateMaintenanceStatus = `
    UPDATE Maintenance
    SET status = ?
    WHERE maintenance_id = ?;
    `;


export const checkRoleAccessInFacility = `
    SELECT *
    FROM Person p JOIN HasAccess a ON p.role_id = a.role_id
    WHERE p.context_broker_id = ? AND a.facility_id = ?;
    `;
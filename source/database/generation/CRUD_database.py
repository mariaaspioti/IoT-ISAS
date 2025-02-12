import os
import csv

# =================================================================================================
# =================== CREATE ======================================================================
# =================================================================================================


def create_roles_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Role (
            role_id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT NOT NULL
        )
    ''')
    return cursor

def create_person_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Person (
            person_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            context_broker_id TEXT,
            role_id INTEGER,
            FOREIGN KEY (role_id) REFERENCES Role(role_id)
        )
    ''')
    return cursor

def create_device_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Device (
            device_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            context_broker_id TEXT,
            description TEXT,
            supportedProtocol TEXT,
            deviceCategory TEXT,
            location_coordinates TEXT,
            direction TEXT,
            directions TEXT,
            value TEXT,
            entry TEXT,
            exit TEXT
        )
    ''')
    return cursor

def create_facility_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Facility (
            facility_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            context_broker_id TEXT,
            description TEXT,
            location_coordinates TEXT,
            category TEXT,
            peopleCapacity INTEGER
        )
    ''')
    return cursor

def create_maintenance_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Maintenance (
            maintenance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            startTime TEXT,
            endTime TEXT,
            dateCreated TEXT,
            status TEXT,
            description TEXT
        )
    ''')
    return cursor

def create_works_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Works (
            works_id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            device_id INTEGER,
            startTime TEXT,
            endTime TEXT,
            date TEXT,
            FOREIGN KEY (person_id) REFERENCES Person(person_id),
            FOREIGN KEY (device_id) REFERENCES Device(device_id)
        )
    ''')
    return cursor

def create_has_access_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS HasAccess (
            role_id INTEGER NOT NULL,
            facility_id INTEGER NOT NULL,
            PRIMARY KEY (role_id, facility_id),
            FOREIGN KEY (role_id) REFERENCES Role(role_id),
            FOREIGN KEY (facility_id) REFERENCES Facility(facility_id)
        )
    ''')
    return cursor

def create_has_assigned_device_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS HasAssignedDevice (
            person_id INTEGER NOT NULL,
            device_id INTEGER NOT NULL,
            PRIMARY KEY (person_id, device_id),
            FOREIGN KEY (person_id) REFERENCES Person(person_id),
            FOREIGN KEY (device_id) REFERENCES Device(device_id)
        )
    ''')
    return cursor

def create_concerns_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Concerns (
            device_id INTEGER NOT NULL,
            facility_id INTEGER NOT NULL,
            PRIMARY KEY (device_id, facility_id),
            FOREIGN KEY (device_id) REFERENCES Device(device_id),
            FOREIGN KEY (facility_id) REFERENCES Facility(facility_id)
        )
    ''')
    return cursor

def create_part_of_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PartOf (
            facility_id INTEGER NOT NULL,
            parent_facility_id INTEGER,
            PRIMARY KEY (facility_id),
            FOREIGN KEY (facility_id) REFERENCES Facility(facility_id),
            FOREIGN KEY (parent_facility_id) REFERENCES Facility(facility_id)
        )
    ''')
    return cursor

def create_conducts_table(cursor):
    # Person conducts maintenance (is exempt from maintenance lock out)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Conducts (
            person_id INTEGER NOT NULL,
            maintenance_id INTEGER NOT NULL,
            PRIMARY KEY (person_id, maintenance_id),
            FOREIGN KEY (person_id) REFERENCES Person(person_id),
            FOREIGN KEY (maintenance_id) REFERENCES Maintenance(maintenance_id)
        )
    ''')
    return cursor

def create_reserves_table(cursor):
    # Maintenance reserves a Facility (locks out the facility)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reserves (
            maintenance_id INTEGER NOT NULL,
            facility_id INTEGER NOT NULL,
            PRIMARY KEY (maintenance_id, facility_id),
            FOREIGN KEY (maintenance_id) REFERENCES Maintenance(maintenance_id),
            FOREIGN KEY (facility_id) REFERENCES Facility(facility_id)
        )
    ''')
    return cursor

def create_all_tables(cursor):
    create_roles_table(cursor)
    create_person_table(cursor)
    create_device_table(cursor)
    create_facility_table(cursor)
    create_maintenance_table(cursor)
    create_works_table(cursor)
    create_has_access_table(cursor)
    create_has_assigned_device_table(cursor)
    create_concerns_table(cursor)
    create_part_of_table(cursor)
    create_conducts_table(cursor)
    create_reserves_table(cursor)
    return cursor

# =================================================================================================
# =================== INSERT ======================================================================
# =================================================================================================

def insert_roles(cursor):
    # Inserting roles
    roles = ["Engineer", "Janitor", "Technician", "Cleanroom Operator"]
    cursor.executemany('''INSERT INTO Role (role_name) VALUES (?)''', [(role,) for role in roles])

    return cursor

def import_persons(cursor):
    person_csv_file = os.path.join(os.path.dirname(__file__), "..", "entities_csv", "Person.csv")
    with open(person_csv_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        persons = [(row['id'], row['name'], row['role']) for row in reader]
        # for 'role' attribute, we need to find the role_id from the Role table
        for person in persons:
            cursor.execute('''SELECT role_id FROM Role WHERE role_name = ?''', (person[2],))
            role_id = cursor.fetchone()[0]
            cursor.execute('''INSERT INTO Person (context_broker_id, name, role_id) VALUES (?, ?, ?)''', (person[0], person[1], role_id))

    return cursor

def import_facilities(cursor):
    building_csv_file = os.path.join(os.path.dirname(__file__), "..", "entities_csv", "Building.csv")
    with open(building_csv_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        facilities = [(
            row['id'], row['name'], row['description'], 
             row['location_coordinates'], row['category'], 
             row['peopleCapacity']) 
             for row in reader
             ]
        cursor.executemany('''INSERT INTO Facility (context_broker_id, name, description, location_coordinates, category, peopleCapacity) VALUES (?, ?, ?, ?, ?, ?)''', facilities)

    return cursor

def import_devices(cursor):
    device_csv_file = os.path.join(os.path.dirname(__file__), "..", "entities_csv", "Device.csv")
    with open(device_csv_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        devices = [(
            row['id'], row['name'], row['description'], 
            row['supportedProtocol'], row['deviceCategory'], 
            row['location_coordinates'], row['direction'], row['directions'], 
            row['value'], row['entry'], row['exit'])
            for row in reader]
        cursor.executemany('''INSERT INTO Device (context_broker_id, name, description, supportedProtocol, deviceCategory, location_coordinates, direction, directions, value, entry, exit) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', devices)

    return cursor

def import_part_of(cursor):
    # read the building csv file
    building_csv_file = os.path.join(os.path.dirname(__file__), "..", "entities_csv", "Building.csv")
    with open(building_csv_file, mode='r', newline='') as file:
        # if the attribute 'partOf' is not empty, find the context_broker_id of the parent building
        reader = csv.DictReader(file)
        for row in reader:
            if row['partOf']:
                cursor.execute('''SELECT facility_id FROM Facility WHERE context_broker_id = ?''', (row['partOf'],))
                parent_facility_id = cursor.fetchone()[0]
                cursor.execute('''SELECT facility_id FROM Facility WHERE context_broker_id = ?''', (row['id'],))
                facility_id = cursor.fetchone()[0]
                cursor.execute('''INSERT INTO PartOf (facility_id, parent_facility_id) VALUES (?, ?)''', (facility_id, parent_facility_id))

    return cursor

def import_has_assigned_device(cursor):
    # read the person csv file
    person_csv_file = os.path.join(os.path.dirname(__file__), "..", "entities_csv", "Person.csv")
    with open(person_csv_file, mode='r', newline='') as file:
        # For all device context_broker_ids in 'hasDevices' attribute, find the device_id and person_id
        reader = csv.DictReader(file)
        for row in reader:
            if row['hasDevices']:
                cursor.execute('''SELECT person_id FROM Person WHERE context_broker_id = ?''', (row['id'],))
                person_id = cursor.fetchone()[0]
                devices = row['hasDevices'].split(";")
                for device in devices:
                    cursor.execute('''SELECT device_id FROM Device WHERE context_broker_id = ?''', (device,))
                    device_id = cursor.fetchone()[0]
                    cursor.execute('''INSERT INTO HasAssignedDevice (person_id, device_id) VALUES (?, ?)''', (person_id, device_id))

    return cursor

def import_concerns(cursor):
    '''For each device, check if it has attributes "entry" and "exit". If it does, find
    their id in the Device table through the context_broker_id and take the value of "entry" and "exit" 
    which contain the context_broker_ids of the corresponding facilities. Together with the device id
    insert the device_id and facility_id into the Concerns table'''
    # read the device csv file
    device_csv_file = os.path.join(os.path.dirname(__file__), "..", "entities_csv", "Device.csv")
    with open(device_csv_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['entry'] and row['exit']:
                cursor.execute('''SELECT device_id FROM Device WHERE context_broker_id = ?''', (row['id'],))
                device_id = cursor.fetchone()[0]
                cursor.execute('''SELECT facility_id FROM Facility WHERE context_broker_id = ?''', (row['entry'],))
                entry_facility_id = cursor.fetchone()[0]
                cursor.execute('''SELECT facility_id FROM Facility WHERE context_broker_id = ?''', (row['exit'],))
                exit_facility_id = cursor.fetchone()[0]
                cursor.execute('''INSERT INTO Concerns (device_id, facility_id) VALUES (?, ?)''', (device_id, entry_facility_id))
                cursor.execute('''INSERT INTO Concerns (device_id, facility_id) VALUES (?, ?)''', (device_id, exit_facility_id))
            elif row['entry']:
                cursor.execute('''SELECT device_id FROM Device WHERE context_broker_id = ?''', (row['id'],))
                device_id = cursor.fetchone()[0]
                cursor.execute('''SELECT facility_id FROM Facility WHERE context_broker_id = ?''', (row['entry'],))
                entry_facility_id = cursor.fetchone()[0]
                cursor.execute('''INSERT INTO Concerns (device_id, facility_id) VALUES (?, ?)''', (device_id, entry_facility_id))
            elif row['exit']:
                cursor.execute('''SELECT device_id FROM Device WHERE context_broker_id = ?''', (row['id'],))
                device_id = cursor.fetchone()[0]
                cursor.execute('''SELECT facility_id FROM Facility WHERE context_broker_id = ?''', (row['exit'],))
                exit_facility_id = cursor.fetchone()[0]
                cursor.execute('''INSERT INTO Concerns (device_id, facility_id) VALUES (?, ?)''', (device_id, exit_facility_id))
            else:
                pass
    return cursor

def insert_has_access(cursor):
    # Get all facilities (fetch facility_id and facility_name)
    cursor.execute('''SELECT facility_id, name FROM Facility''')
    facilities = cursor.fetchall()
    
    # Mapping facility names to IDs
    facility_mapping = {facility[1]: facility[0] for facility in facilities}
    
    # Defining which facilities each role has access to
    engineer_facilities = ["Cleanroom 1", "Cleanroom 2", "Cleanroom 3", "Cleanroom 4", "FAB 1", "FAB 2", "FAB 10", "FAB 14", "FAB 10 ENERGY CENTRE", "FAB 14 ENERGY CENTRE", "R&D", "Ryebrook 110kV Substation"]
    technician_facilities = ["FAB 1", "FAB 2", "FAB 10", "FAB 14", "R&D", "Waste Water Treatment Building", "Water Treatment Building"]
    cleanroom_facilities = ["Cleanroom 1", "Cleanroom 2", "Cleanroom 3", "Cleanroom 4", "FAB 1", "FAB 2", "FAB 10", "FAB 14"]
    janitor_facilities = list(facility_mapping.keys())  # Janitors have access to all facilities

    # Get all roles and map role names to IDs
    cursor.execute('''SELECT role_id, role_name FROM Role''')
    roles = cursor.fetchall()
    
    role_mapping = {role[1]: role[0] for role in roles}
    
    # Associate each role with the facilities they have access to
    for role_name, role_id in role_mapping.items():
        if role_name == "Engineer":
            for facility_name in engineer_facilities:
                cursor.execute('''INSERT INTO HasAccess (role_id, facility_id) VALUES (?, ?)''', (role_id, facility_mapping[facility_name]))
        elif role_name == "Janitor":
            for facility_name in janitor_facilities:
                cursor.execute('''INSERT INTO HasAccess (role_id, facility_id) VALUES (?, ?)''', (role_id, facility_mapping[facility_name]))
        elif role_name == "Technician":
            for facility_name in technician_facilities:
                cursor.execute('''INSERT INTO HasAccess (role_id, facility_id) VALUES (?, ?)''', (role_id, facility_mapping[facility_name]))
        elif role_name == "Cleanroom Operator":
            for facility_name in cleanroom_facilities:
                cursor.execute('''INSERT INTO HasAccess (role_id, facility_id) VALUES (?, ?)''', (role_id, facility_mapping[facility_name]))

    return cursor

def insert_all_data(cursor):
    insert_roles(cursor)
    import_persons(cursor)
    import_facilities(cursor)
    import_devices(cursor)
    import_part_of(cursor)
    import_has_assigned_device(cursor)
    import_concerns(cursor)
    insert_has_access(cursor)
    return cursor


# =================================================================================================
# =================== DELETE ======================================================================
# =================================================================================================

def delete_roles(cursor):
    cursor.execute('''DELETE FROM Role''')
    return cursor

def delete_persons(cursor):
    cursor.execute('''DELETE FROM Person''')
    return cursor

def delete_facilities(cursor):
    cursor.execute('''DELETE FROM Facility''')
    return cursor

def delete_devices(cursor):
    cursor.execute('''DELETE FROM Device''')
    return cursor

def delete_part_of(cursor):
    cursor.execute('''DELETE FROM PartOf''')
    return cursor

def delete_has_assigned_device(cursor):
    cursor.execute('''DELETE FROM HasAssignedDevice''')
    return cursor

def delete_concerns(cursor):
    cursor.execute('''DELETE FROM Concerns''')
    return cursor

def delete_has_access(cursor):
    cursor.execute('''DELETE FROM HasAccess''')
    return cursor

def delete_conducts(cursor):
    cursor.execute('''DELETE FROM Conducts''')
    return cursor

def delete_reserves(cursor):
    cursor.execute('''DELETE FROM Reserves''')
    return cursor

def delete_maintenance(cursor):
    cursor.execute('''DELETE FROM Maintenance''')
    return cursor

def delete_maintenance_conducts_reserves(cursor):
    # also delete from Conducts and Reserves and Maintenance
    delete_conducts(cursor)
    delete_reserves(cursor)
    delete_maintenance(cursor)
    return cursor

def delete_all_tables(cursor):
    delete_has_access(cursor)
    delete_concerns(cursor)
    delete_has_assigned_device(cursor)
    delete_part_of(cursor)
    delete_devices(cursor)
    delete_facilities(cursor)
    delete_persons(cursor)
    delete_roles(cursor)
    delete_maintenance_conducts_reserves(cursor)
    return cursor

def drop_all_tables(cursor):
    cursor.execute('''DROP TABLE IF EXISTS Person''')
    cursor.execute('''DROP TABLE IF EXISTS Role''')
    cursor.execute('''DROP TABLE IF EXISTS Device''')
    cursor.execute('''DROP TABLE IF EXISTS Facility''')
    cursor.execute('''DROP TABLE IF EXISTS Maintenance''')
    cursor.execute('''DROP TABLE IF EXISTS Works''')
    cursor.execute('''DROP TABLE IF EXISTS HasAccess''')
    cursor.execute('''DROP TABLE IF EXISTS HasAssignedDevice''')
    cursor.execute('''DROP TABLE IF EXISTS Concerns''')
    cursor.execute('''DROP TABLE IF EXISTS PartOf''')
    cursor.execute('''DROP TABLE IF EXISTS Conducts''')
    cursor.execute('''DROP TABLE IF EXISTS Reserves''')
    return cursor
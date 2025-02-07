import os
import csv

def insert_roles(cursor):
    # Inserting roles
    roles = ["Engineer", "Janitor", "Technician", "Cleanroom Operator"]
    cursor.executemany('''INSERT INTO Role (role_name) VALUES (?)''', [(role,) for role in roles])

    return cursor

def import_persons(cursor):
    person_csv_file = os.path.join(os.path.dirname(__file__), "..", "entities_csv", "Person.csv")
    with open(person_csv_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        persons = [(row['id'], row['name']) for row in reader]
        cursor.executemany('''INSERT INTO Person (context_broker_id, name) VALUES (?, ?)''', persons)

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
            row['value']) 
            for row in reader]
        cursor.executemany('''INSERT INTO Device (context_broker_id, name, description, supportedProtocol, deviceCategory, location_coordinates, direction, directions, value) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', devices)

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
    # read the device csv file
    device_csv_file = os.path.join(os.path.dirname(__file__), "..", "entities_csv", "Device.csv")
    with open(device_csv_file, mode='r', newline='') as file:
        # For all device context_broker_ids in 'concerns' attribute, find the device_id and facility_id
        reader = csv.DictReader(file)
        for row in reader:
            if row['concerns']:
                cursor.execute('''SELECT device_id FROM Device WHERE context_broker_id = ?''', (row['id'],))
                device_id = cursor.fetchone()[0]
                facilities = row['concerns'].split(";")
                for facility in facilities:
                    cursor.execute('''SELECT facility_id FROM Facility WHERE context_broker_id = ?''', (facility,))
                    facility_id = cursor.fetchone()[0]
                    cursor.execute('''INSERT INTO Concerns (device_id, facility_id) VALUES (?, ?)''', (device_id, facility_id))

    return cursor

def insert_has_access(cursor):
    # Get all facilities (fetch facility_id and facility_name)
    cursor.execute('''SELECT facility_id, facility_name FROM Facility''')
    facilities = cursor.fetchall()
    
    # Mapping facility names to IDs
    facility_mapping = {facility[1]: facility[0] for facility in facilities}
    
    # Defining which facilities each role has access to
    engineer_facilities = ["FAB 1", "FAB 2", "FAB 10", "FAB 14", "FAB 10 ENERGY CENTRE", "FAB 14 ENERGY CENTRE", "R&D", "Ryebrook 110kV Substation"]
    technician_facilities = ["FAB 1", "FAB 2", "FAB 10", "FAB 14", "R&D", "Waste Water Treatment Building", "Water Treatment Building"]
    cleanroom_facilities = ["CLEANROOM 1", "CLEANROOM 3", "CLEANROOM 4", "FAB 1", "FAB 2", "FAB 10", "FAB 14"]
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


    
import sqlite3

def create_database():
    conn = sqlite3.connect("ISAS_database.db")
    cursor = conn.cursor()
    
    # Creating tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Person (
            person_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            context_broker_id TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Role (
            role_id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Device (
            device_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            context_broker_id TEXT,
            description TEXT,
            supportedProtocol TEXT,
            deviceCategory TEXT,
            location_coordinates TEXT
            direction TEXT,
            directions TEXT,
            value TEXT,
        )
    ''')
    
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
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Maintenance (
            maintenance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER,
            startTime TEXT,
            endTime TEXT,
            dateCreated TEXT,
            FOREIGN KEY (device_id) REFERENCES Device(device_id)
        )
    ''')
    
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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS HasAccess (
            person_id INTEGER NOT NULL,
            facility_id INTEGER NOT NULL,
            PRIMARY KEY (person_id, facility_id),
            FOREIGN KEY (person_id) REFERENCES Person(person_id),
            FOREIGN KEY (facility_id) REFERENCES Facility(facility_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS HasAssignedDevice (
            person_id INTEGER NOT NULL,
            device_id INTEGER NOT NULL,
            PRIMARY KEY (person_id, device_id),
            FOREIGN KEY (person_id) REFERENCES Person(person_id),
            FOREIGN KEY (device_id) REFERENCES Device(device_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Concerns (
            device_id INTEGER NOT NULL,
            facility_id INTEGER NOT NULL,
            PRIMARY KEY (device_id, facility_id),
            FOREIGN KEY (device_id) REFERENCES Device(device_id),
            FOREIGN KEY (facility_id) REFERENCES Facility(facility_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PartOf (
            facility_id INTEGER NOT NULL,
            parent_facility_id INTEGER,
            PRIMARY KEY (facility_id),
            FOREIGN KEY (facility_id) REFERENCES Facility(facility_id),
            FOREIGN KEY (parent_facility_id) REFERENCES Facility(facility_id)
        )
    ''')
        
    # # Mapping roles to IDs
    # cursor.execute("SELECT role_id, role_name FROM Role")
    # role_mapping = {name: role_id for role_id, name in cursor.fetchall()}
    
    # # Inserting persons with correct role IDs
    # persons = [
    #     ("Elizabeth Franklin"),
    #     ("Scott Reynolds"),
    #     ("Michael Stewart"),
    #     ("Wanda Brandt"),
    #     ("Angelica Smith"),
    #     ("Lauren Riley"),
    #     ("Christine Herman MD"),
    #     ("Julian Jordan"),
    #     ("Devin Martinez"),
    #     ("Kevin Williams"),
    #     ("Rebecca Glenn")
    # ]
    # cursor.executemany('''INSERT INTO Person (name) VALUES (?)''', persons)
    
    # # Inserting devices
    # devices = [
    #     ("Device 1", "Description for Device 1", "Protocol A", "Category 1", "Coord1"),
    #     ("Device 2", "Description for Device 2", "Protocol B", "Category 2", "Coord2"),
    #     ("Device 3", "Description for Device 3", "Protocol C", "Category 3", "Coord3")
    # ]
    # cursor.executemany('''INSERT INTO Device (name, description, supportedProtocol, deviceCategory, location_coord) VALUES (?, ?, ?, ?, ?)''', devices)

    # # Inserting facilities
    # facilities = [
    #     ("REMF", "Facility Description", "Coord1", "Category A", 100),
    #     ("FAB 1", "Facility Description", "Coord2", "Category B", 150)
    #     # Add more facilities here
    # ]
    # cursor.executemany('''INSERT INTO Facility (name, description, location_coord, category, peopleCapacity) VALUES (?, ?, ?, ?, ?)''', facilities)

    # # Mapping persons to IDs
    # cursor.execute("SELECT person_id, name FROM Person")
    # person_mapping = {name: person_id for person_id, name in cursor.fetchall()}
    
    # # Mapping devices to IDs
    # cursor.execute("SELECT device_id, name FROM Device")
    # device_mapping = {name: device_id for device_id, name in cursor.fetchall()}
    
    # # Mapping facilities to IDs
    # cursor.execute("SELECT facility_id, name FROM Facility")
    # facility_mapping = {name: facility_id for facility_id, name in cursor.fetchall()}
    
    # # Assigning facility access based on roles
    # access_entries = []
    # for person, role_id in persons:
    #     if role_id == role_mapping["Engineer"]:
    #         # Example: assign specific devices and facilities based on roles
    #         access_entries.append((person_mapping[person], facility_mapping["FAB 1"]))
    
    # cursor.executemany('''INSERT INTO HasAccess (person_id, facility_id) VALUES (?, ?)''', access_entries)

    # # Example: Assign devices to people
    # device_assignments = [(person_mapping["Elizabeth Franklin"], device_mapping["Device 1"])]
    # cursor.executemany('''INSERT INTO HasAssignedDevice (person_id, device_id) VALUES (?, ?)''', device_assignments)
    
    conn.commit()
    conn.close()
    print("Database and tables created successfully with roles, persons, devices, facilities, and access rights.")

def main():
    create_database()

if __name__ == "__main__":
    main()

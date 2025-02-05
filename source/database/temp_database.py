import sqlite3

def create_database():
    conn = sqlite3.connect("ISAS_database.db")
    cursor = conn.cursor()
    
    # Creating tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Person (
            person_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role_id INTEGER,
            FOREIGN KEY (role_id) REFERENCES Role(role_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Role (
            role_id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT NOT NULL
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
        CREATE TABLE IF NOT EXISTS Facility (
            facility_id INTEGER PRIMARY KEY AUTOINCREMENT,
            facility_name TEXT NOT NULL
        )
    ''')
    
    # Inserting facilities
    facilities = [
        "REMF", "FAB 1", "CLEANROOM 1", "FAB 2", "FAB 10", "CLEANROOM 3", "FAB 14", 
        "CLEANROOM 4", "FAB 10 ENERGY CENTRE", "FAB 14 ENERGY CENTRE", "R&D", "IR5", 
        "IR2", "RODI", "ASU", "Ryebrook 110kV Substation", "Waste Water Treatment Building", 
        "Water Treatment Building", "MSCP"
    ]
    cursor.executemany('''INSERT INTO Facility (facility_name) VALUES (?)''', [(facility,) for facility in facilities])
    
    # Inserting roles
    roles = ["Engineer", "Janitor", "Technician", "Cleanroom Operator"]
    cursor.executemany('''INSERT INTO Role (role_name) VALUES (?)''', [(role,) for role in roles])
    
    # Mapping roles to IDs
    cursor.execute("SELECT role_id, role_name FROM Role")
    role_mapping = {name: role_id for role_id, name in cursor.fetchall()}
    
    # Inserting persons with correct role IDs
    persons = [
        ("Elizabeth Franklin", role_mapping["Engineer"]),
        ("Scott Reynolds", role_mapping["Janitor"]),
        ("Michael Stewart", role_mapping["Technician"]),
        ("Wanda Brandt", role_mapping["Cleanroom Operator"]),
        ("Angelica Smith", role_mapping["Technician"]),
        ("Lauren Riley", role_mapping["Engineer"]),
        ("Christine Herman MD", role_mapping["Cleanroom Operator"]),
        ("Julian Jordan", role_mapping["Cleanroom Operator"]),
        ("Devin Martinez", role_mapping["Technician"]),
        ("Kevin Williams", role_mapping["Engineer"]),
        ("Rebecca Glenn", role_mapping["Cleanroom Operator"])
    ]
    cursor.executemany('''INSERT INTO Person (name, role_id) VALUES (?, ?)''', persons)
    
    # Mapping persons to IDs
    cursor.execute("SELECT person_id, name FROM Person")
    person_mapping = {name: person_id for person_id, name in cursor.fetchall()}
    
    # Mapping facilities to IDs
    cursor.execute("SELECT facility_id, facility_name FROM Facility")
    facility_mapping = {name: facility_id for facility_id, name in cursor.fetchall()}
    
    # Assigning facility access based on roles
    access_entries = []
    
    engineer_facilities = ["FAB 1", "FAB 2", "FAB 10", "FAB 14", "FAB 10 ENERGY CENTRE", "FAB 14 ENERGY CENTRE", "R&D", "Ryebrook 110kV Substation"]
    technician_facilities = ["FAB 1", "FAB 2", "FAB 10", "FAB 14", "R&D", "Waste Water Treatment Building", "Water Treatment Building"]
    cleanroom_facilities = ["CLEANROOM 1", "CLEANROOM 3", "CLEANROOM 4", "FAB 1", "FAB 2", "FAB 10", "FAB 14"]
    janitor_facilities = facilities  # Janitors have access to all
    
    for person, role_id in persons:
        if role_id == role_mapping["Engineer"]:
            access_entries.extend((person_mapping[person], facility_mapping[fac]) for fac in engineer_facilities)
        elif role_id == role_mapping["Technician"]:
            access_entries.extend((person_mapping[person], facility_mapping[fac]) for fac in technician_facilities)
        elif role_id == role_mapping["Cleanroom Operator"]:
            access_entries.extend((person_mapping[person], facility_mapping[fac]) for fac in cleanroom_facilities)
        elif role_id == role_mapping["Janitor"]:
            access_entries.extend((person_mapping[person], facility_mapping[fac]) for fac in janitor_facilities)
    
    cursor.executemany('''INSERT INTO HasAccess (person_id, facility_id) VALUES (?, ?)''', access_entries)
    
    conn.commit()
    conn.close()
    print("Database and tables created successfully with facilities, roles, persons, and access rights.")

if __name__ == "__main__":
    create_database()
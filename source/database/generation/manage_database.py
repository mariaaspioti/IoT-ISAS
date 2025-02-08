import sqlite3
import os
import sys
import json
import numpy as np

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import CRUD_database as CRUD

def connect_to_database(path):
    database_path = path
    try:
        conn = sqlite3.connect(database_path)
        return conn
    except sqlite3.Error as e:
        print(e)
        return None
    
def insert_data(cursor):
    cursor = CRUD.insert_all_data(cursor)
    return cursor

def test_func():
    # Connect to database
    conn = connect_to_database(os.path.join(os.path.dirname(__file__), "..", "ISAS_database.db"))
    cursor = conn.cursor()

    print("No action")

    # Close the connection
    conn.close()

def menu_options():
    print("1. Create all tables")
    print("2. Drop all tables")
    print("3. Insert data into tables")
    print("4. Delete data from tables")
    print("5. Run test function")
    print("6. Press q to Exit")
    return input("> ")

def main():
    while True:
        choice = menu_options()
        if choice == "q" or choice == "Q":
            print("Exiting...")
            break
        conn = connect_to_database(os.path.join(os.path.dirname(__file__), "..", "ISAS_database.db"))
        if conn is None:
            print("Failed to connect to the database.")
            continue
        cursor = conn.cursor()
        if choice == "1":
            CRUD.create_all_tables(cursor)
            conn.commit()
            print("All tables created successfully.")
        elif choice == "2":
            CRUD.drop_all_tables(cursor)
            conn.commit()
            print("All tables dropped successfully.")
        elif choice == "3":
            insert_data(cursor)
            conn.commit()
            print("Data inserted successfully.")
        elif choice == "4":
            CRUD.delete_all_tables(cursor)
            conn.commit()
            print("Data deleted successfully.")
        elif choice == "4":
            test_func()
        else:
            print("Invalid choice. Please try again.")
        conn.close()

if __name__ == "__main__":
    main()
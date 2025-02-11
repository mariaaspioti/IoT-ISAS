import requests
import json
import os

# Orion Context Broker details
orion_url = "http://150.140.186.118:1026/v2/entities"
fiware_service = "ISAS"
fiware_service_path = "/test"

# POST/PATCH headers
pp_headers = {
    "Content-Type": "application/json",
    "Fiware-Service": fiware_service,
    "Fiware-ServicePath": fiware_service_path
}

# GET/DELETE headers
gd_headers = {
    "Fiware-Service": fiware_service,
    "Fiware-ServicePath": fiware_service_path
}

backup_file = "backup_serial_numbers.json"

def get_device_serial_number(device_id):
    url = f"{orion_url}/{device_id}"
    response = requests.get(url, headers=gd_headers)
    if response.status_code == 200:
        data = response.json()
        serial_number = data['serialNumber']['value']
        return serial_number
    else:
        print(f"Error fetching data for {device_id}: {response.status_code}")
        return None

def change_device_serial_number(device_id, new_serial_number):
    command_url = f"{orion_url}/{device_id}/attrs"
    command_payload = {
        "serialNumber": {
            "type": "Text",
            "value": new_serial_number
        }
    }
    try:
        response = requests.patch(command_url, headers=pp_headers, json=command_payload)
        if response.status_code == 204:
            print(f"Serial number for device {device_id} changed successfully to {new_serial_number}")
        else:
            print(f"Failed to change serial number for device {device_id}: {response.status_code}")
    except Exception as e:
        print(f"Error changing serial number for device {device_id}: {e}")

def backup_serial_number(device_id, old_serial_number):
    backup_data = {}
    if os.path.exists(backup_file):
        with open(backup_file, "r") as file:
            backup_data = json.load(file)
    
    backup_data[device_id] = old_serial_number
    
    with open(backup_file, "w") as file:
        json.dump(backup_data, file, indent=4)
    print(f"Backup saved for device {device_id}")

def restore_serial_number(device_id):
    if not os.path.exists(backup_file):
        print("No backup file found")
        return
    
    with open(backup_file, "r") as file:
        backup_data = json.load(file)
    
    if device_id in backup_data:
        old_serial_number = backup_data[device_id]
        change_device_serial_number(device_id, old_serial_number)
        print(f"Serial number for device {device_id} restored to {old_serial_number}")
    else:
        print(f"No backup found for device {device_id}")

def main():
    restore_serial_number("urn:ngsi-ld:Device:91")
    # device_id = input("Enter the device ID: ")
    # new_serial_number = input("Enter the new serial number: ")
    
    # old_serial_number = get_device_serial_number(device_id)
    # if old_serial_number:
    #     backup_serial_number(device_id, old_serial_number)
    #     change_device_serial_number(device_id, new_serial_number)

if __name__ == "__main__":
    main()
    
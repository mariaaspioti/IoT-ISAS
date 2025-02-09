import requests
import time
import os
from dotenv import load_dotenv

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

# REAL Smart Lock Functions


# Load environment variables from the .env file in the parent 'source' directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

def unlock_smartlock():
    token = os.getenv('AUTH_TOKEN')
    if not token:
        raise ValueError("No token found in the environment variables")

    url = 'https://api.nuki.io/smartlock/18043712356/action/unlock'
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json',  # Add 'accept' header for consistency
    }

    # No payload sent
    response = requests.post(url, headers=headers)

    if response.status_code == 204:
        print('Unlock request was successful')
    else:
        print('Unlock request failed')
        print('Status code:', response.status_code)
        print('Response:', response.text)


def lock_smartlock():
    token = os.getenv('AUTH_TOKEN')
    if not token:
        raise ValueError("No token found in the environment variables")

    url = 'https://api.nuki.io/smartlock/18043712356/action/lock'
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json',  # Add 'accept' header for consistency
    }

    # No payload sent
    response = requests.post(url, headers=headers)

    if response.status_code == 204:
        print('Lock request was successful')
    else:
        print('Lock request failed')
        print('Status code:', response.status_code)
        print('Response:', response.text)
        
def get_smartlock_():
    token = os.getenv('AUTH_TOKEN')

    if not token:
        raise ValueError("No token found in the environment variables")
    
    url = 'https://api.nuki.io/smartlock'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}',
       
    }

    response = requests.get(url, headers=headers)

    # Print the response status code and JSON content
    print(response.status_code)
    print(response.json())

# ALL Smart Lock Functions

def get_all_smart_locks():
    url = f"{orion_url}?type=Device&q=name~=^SmartLock-"
    response = requests.get(url, headers=gd_headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching smart locks: {response.status_code}")
        return []

def get_smart_lock_state(smart_lock_id):
    url = f"{orion_url}/{smart_lock_id}"
    response = requests.get(url, headers=gd_headers)
    if response.status_code == 200:
        data = response.json()
        value = data['value']['value']
        device_state = data['deviceState']['value']
        return value, device_state
    else:
        print(f"Error fetching data for {smart_lock_id}: {response.status_code}")
        return None, None

def send_lock_command(smart_lock_id):
    command_url = f"{orion_url}/{smart_lock_id}/attrs"
    command_payload = {
        "deviceState": {
                    "type": "Text",
                    "value": "locked"
                },
                "value": {
                    "type": "Text",
                    "value": "2"
                },
                "dateLastValueReported": {
                    "type": "DateTime",
                    "value": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
                },
            }
    try:
        response = requests.patch(command_url, headers=pp_headers, json=command_payload)
        if response.status_code == 204:
            print(f"Smart lock {smart_lock_id} locked successfully")
        else:
            print(f"Failed to lock smart lock {smart_lock_id}: {response.status_code}")
    except Exception as e:
        print(f"Error sending lock command to smart lock: {e}")

def initialize_smart_lock_states():
    last_states = {}
    smart_locks = get_all_smart_locks()
    for smart_lock in smart_locks:
        smart_lock_id = smart_lock['id']
        value, device_state = get_smart_lock_state(smart_lock_id)
        if value is not None and device_state is not None:
            last_states[smart_lock_id] = (value, device_state)
    return last_states

def monitor_smart_locks():
    last_states = initialize_smart_lock_states()

    while True:
        smart_locks = get_all_smart_locks()
        for smart_lock in smart_locks:
            smart_lock_id = smart_lock['id']
            value, device_state = get_smart_lock_state(smart_lock_id)
            if value is not None and device_state is not None:
                last_value, last_device_state = last_states.get(smart_lock_id, (None, None))
                if value != last_value or device_state != last_device_state:
                    print(f"Smart Lock {smart_lock_id} - Value: {value}, Device State: {device_state}")
                    last_states[smart_lock_id] = (value, device_state)
                    if device_state == "unlocked":
                        if (smart_lock['serialNumber']['value']=='18043712356'):
                            print(smart_lock['serialNumber']['value'])
                            unlock_smartlock()
                            print(f"Smart Lock {smart_lock_id} unlocked, will lock again in 10 seconds")
                            time.sleep(10)
                            send_lock_command(smart_lock_id)
                            lock_smartlock()
                        else:
                            print(f"Smart Lock {smart_lock_id} unlocked, will lock again in 10 seconds")
                            time.sleep(10)
                            send_lock_command(smart_lock_id)
                    else:
                        print("Device is already unlocked")       
        time.sleep(5)


def send_lock_command_to_device(device_id):
    command_url = f"{orion_url}/{device_id}/attrs"
    command_payload = {
        "deviceState": {
            "type": "Text",
            "value": "locked"
        },
        "value": {
            "type": "Text",
            "value": "2"
        },
        "dateLastValueReported": {
            "type": "DateTime",
            "value": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
        }
    }
    try:
        response = requests.patch(command_url, headers=pp_headers, json=command_payload)
        if response.status_code == 204:
            print(f"Smart lock {device_id} locked successfully")
        else:
            print(f"Failed to lock smart lock {device_id}: {response.status_code}")
    except Exception as e:
        print(f"Error sending lock command to smart lock {device_id}: {e}")

def main():
    try:
        print("Starting IoT Agent for Smart Locks...")
        # monitor_smart_locks()
        send_lock_command_to_device("urn:ngsi-ld:Device:91")
    except KeyboardInterrupt:
        print("Shutting down")


if __name__ == "__main__":
    main()
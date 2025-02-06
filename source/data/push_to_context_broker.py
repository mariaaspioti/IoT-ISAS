import requests
import json
import os

# Base path for the JSON files, "data_generation" is the folder containing the JSON files
base_path = os.path.join(os.path.dirname(__file__), "data_generation")

# Orion Context Broker URL
orion_url = "http://150.140.186.118:1026/v2/entities"
fiware_service = "ISAS"
fiware_service_path = "/test"
# POST headers
post_headers = {
    "Content-Type": "application/json",
    "Fiware-Service": fiware_service,
    "Fiware-ServicePath": fiware_service_path
}
# GET/DELETE headers
gd_headers = {
    "Fiware-Service": fiware_service,
    "Fiware-ServicePath": fiware_service_path
}

def post_building_entities():
    '''Post Building entities to the Context Broker'''
    with open(os.path.join(base_path, "buildings.json")) as f:
        entities = json.load(f) 
        for entity in entities:
            if entity["name"]["value"] == "Waste Water Treatment Building":
                print(f"Entity: {entity}")
                input("Press Enter to continue...")
            response = requests.post(orion_url, headers=post_headers, json=entity)
            if response.status_code == 201:
                print(f"Entity {entity['id']} created successfully")
            elif response.status_code == 422:
                print(f"Entity {entity['id']} already exists")
            else:
                print(f"Failed to create entity {entity['id']} with status code {response.status_code}, response: {response.text}")

    # test validity
    get_headers = {
        "Fiware-Service": fiware_service,
        "Fiware-ServicePath": fiware_service_path
    }
    response = requests.get(orion_url, headers=get_headers)
    if response.status_code == 200:
        print("Entities retrieved successfully")
        print(response.json())
    else:
        print("Failed to retrieve entities")
    

def post_person_entities():
    '''Post Person entities to the Context Broker'''
    with open(os.path.join(base_path, "people.json")) as f:
        entities = json.load(f)
        for entity in entities:
            response = requests.post(orion_url, headers=post_headers, json=entity)
            if response.status_code == 201:
                print(f"Entity {entity['id']} created successfully")
            elif response.status_code == 422:
                print(f"Entity {entity['id']} already exists")
            else:
                print(f"Failed to create entity {entity['id']} with status code {response.status_code}, response: {response.text}")

    # test validity
    response = requests.get(orion_url, headers=gd_headers)
    if response.status_code == 200:
        print("Entities retrieved successfully")
        print(response.json())
    else:
        print("Failed to retrieve entities")

def post_device_trackers_entities():
    '''Post Device entities to the Context Broker'''
    with open(os.path.join(base_path, "devices_trackers.json")) as f:
        entities = json.load(f)
        for entity in entities:
            response = requests.post(orion_url, headers=post_headers, json=entity)
            if response.status_code == 201:
                print(f"Entity {entity['id']} created successfully")
            elif response.status_code == 422:
                print(f"Entity {entity['id']} already exists")
            else:
                print(f"Failed to create entity {entity['id']} with status code {response.status_code}, response: {response.text}")

    # test validity
    response = requests.get(orion_url, headers=gd_headers)
    if response.status_code == 200:
        print("Entities retrieved successfully")
        print(response.json())
    else:
        print("Failed to retrieve entities")

def post_door_entities():
    '''Post Door entities to the Context Broker'''
    with open(os.path.join(base_path, "doors.json")) as f:
        entities = json.load(f)
        for entity in entities:
            response = requests.post(orion_url, headers=post_headers, json=entity)
            if response.status_code == 201:
                print(f"Entity {entity['id']} created successfully")
            elif response.status_code == 422:
                print(f"Entity {entity['id']} already exists")
            else:
                print(f"Failed to create entity {entity['id']} with status code {response.status_code}, response: {response.text}")

    # test validity
    response = requests.get(orion_url, headers=gd_headers)
    if response.status_code == 200:
        print("Entities retrieved successfully")
        print(response.json())
    else:
        print("Failed to retrieve entities")


def post_nfc_reader_entities():
    '''Post NFC Reader entities to the Context Broker'''
    with open(os.path.join(base_path, "nfc_readers.json")) as f:
        entities = json.load(f)
        for entity in entities:
            response = requests.post(orion_url, headers=post_headers, json=entity)
            if response.status_code == 201:
                print(f"Entity {entity['id']} created successfully")
            elif response.status_code == 422:
                print(f"Entity {entity['id']} already exists")
            else:
                print(f"Failed to create entity {entity['id']} with status code {response.status_code}, response: {response.text}")

    # test validity
    response = requests.get(orion_url, headers=gd_headers)
    if response.status_code == 200:
        print("Entities retrieved successfully")
        print(response.json())
    else:
        print("Failed to retrieve entities")

def post_smart_lock_entities():
    '''Post Smart Lock entities to the Context Broker'''
    with open(os.path.join(base_path, "smart_locks.json")) as f:
        entities = json.load(f)
        for entity in entities:
            response = requests.post(orion_url, headers=post_headers, json=entity)
            if response.status_code == 201:
                print(f"Entity {entity['id']} created successfully")
            elif response.status_code == 422:
                print(f"Entity {entity['id']} already exists")
            else:
                print(f"Failed to create entity {entity['id']} with status code {response.status_code}, response: {response.text}")

    # test validity
    response = requests.get(orion_url, headers=gd_headers)
    if response.status_code == 200:
        print("Entities retrieved successfully")
        print(response.json())
    else:
        print("Failed to retrieve entities")

def post_sos_button_entities():
    '''Post SOS Button entities to the Context Broker'''
    with open(os.path.join(base_path, "SOSbuttons.json")) as f:
        entities = json.load(f)
        for entity in entities:
            response = requests.post(orion_url, headers=post_headers, json=entity)
            if response.status_code == 201:
                print(f"Entity {entity['id']} created successfully")
            elif response.status_code == 422:
                print(f"Entity {entity['id']} already exists")
            else:
                print(f"Failed to create entity {entity['id']} with status code {response.status_code}, response: {response.text}")

    # test validity
    response = requests.get(orion_url, headers=gd_headers)
    if response.status_code == 200:
        print("Entities retrieved successfully")
        print(response.json())
    else:
        print("Failed to retrieve entities")

def delete_in_path():
    '''Delete all entities in the given path'''
    print(f"About to delete all entities in path: {fiware_service_path}. Are you sure? (y/n)")
    userin = input()
    if userin != "y":
        print("Cancelled")
        return
    # get all entities in the given path
    limit = 1000
    delete_alarms = False
    response = requests.get(orion_url + "?limit=" + str(limit), headers=gd_headers)
    if response.status_code == 200:
        entities = response.json()
        for entity in entities:
            if entity["type"] == "Alarm" and not delete_alarms:
                print(f"Do you want to delete Alarm entities too? (y/n):")
                userin = input()
                if userin != "y":
                    continue
                else:
                    delete_alarms = True
            response = requests.delete(orion_url + "/" + entity["id"], headers=gd_headers)
            if response.status_code == 204:
                print(f"Entity {entity['id']} deleted successfully")
            else:
                print(f"Failed to delete entity {entity['id']}")
    else:
        print("Failed to retrieve entities")

def delete_alert_entities():
    '''Delete all Alert entities in the given path'''
    print(f"About to delete all Alert entities in path: {fiware_service_path}. Are you sure? (y/n)")
    userin = input()
    if userin != "y":
        print("Cancelled")
        return
    # get all entities in the given path
    limit = 1000
    response = requests.get(orion_url + "?type=Alert&limit=" + str(limit), headers=gd_headers)
    if response.status_code == 200:
        entities = response.json()
        for entity in entities:
            response = requests.delete(orion_url + "/" + entity["id"], headers=gd_headers)
            if response.status_code == 204:
                print(f"Entity {entity['id']} deleted successfully")
            else:
                print(f"Failed to delete entity {entity['id']}")
    else:
        print("Failed to retrieve entities")

def main():
    print("Press:") 
    print("1. To create all entities\n2. To delete alert entities.\n3. To To delete entities in the test path\n4. Type 'q' to exit: ")
    userin = input()
    if userin == "q":
        return
    if userin == "1":
        post_building_entities()
        post_person_entities()
        post_device_trackers_entities()
        post_door_entities()
        post_nfc_reader_entities()
        post_sos_button_entities()
        post_smart_lock_entities()
        return
    if userin == "2":
        delete_alert_entities()
        return
    if userin == "3":
        delete_in_path()
        return
    print("Invalid input")

if __name__ == "__main__":
    main()
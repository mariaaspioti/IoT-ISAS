import requests
import json

# Orion Context Broker URL
orion_url = "http://150.140.186.118:1026/v2/entities"
fiware_service_path = "/ISAS/test"

def create_entity(entity):
    """Sends a POST request to the Context Broker to create an entity."""
    headers = {
        "Content-Type": "application/json",
        
        "Fiware-ServicePath": fiware_service_path
    }

    response = requests.post(orion_url, headers=headers, data=json.dumps(entity))
    if response.status_code == 201:
        print(f"Entity {entity['id']} created successfully.")
    elif response.status_code == 422:  # Entity already exists
        print(f"Entity {entity['id']} already exists.")
    else:
        print(f"Failed to create entity {entity['id']}. Status code: {response.status_code}, Error: {response.text}")

# Create Building Entity
def create_building():
    building = {
        "id": "urn:Building:facility001",
        "type": "Building",
        "name": {
            "type": "Text",
            "value": "Main Warehouse"
        },
        "location": {
            "type": "geo:json",
            "value": {
                "type": "Point",
                "coordinates": [21.788930292, 38.288395556]
            }
        },
        "category": {
            "type": "Text",
            "value": "warehouse"
        }
    }
    create_entity(building)

# Create Person Entity
def create_person(worker_id, device_id, building_id):
    person = {
        "id": f"urn:Person:{worker_id}",
        "type": "Person",
        "name": {
            "type": "Text",
            "value": "Worker " + worker_id
        },
        "hasDevice": {
            "type": "Relationship",
            "value": f"urn:Device:{device_id}"
        },
        "currentFacility": {
            "type": "Relationship",
            "value": building_id
        },
        "location": {
            "type": "geo:json",
            "value": {
                "type": "Point",
                "coordinates": [21.788930292, 38.288395556]
            }
        }
    }
    create_entity(person)

# Create Device Entity
def create_device(device_id, location_coordinates):
    device = {
        "id": f"urn:Device:{device_id}",
        "type": "Device",
        "name": {
            "type": "Text", 
            "value": f"Tracker {device_id}"
            },
        "location": {
            "type": "geo:json",
            "value": {
                "type": "Point", 
                "coordinates": location_coordinates
                },
        },
    }
    create_entity(device)

def delete_entity(entity_id):
    """Sends a DELETE request to the Context Broker to delete an entity."""
    headers = {
        "Fiware-ServicePath": fiware_service_path
    }
    response = requests.delete(orion_url + f"/{entity_id}", headers=headers)
    if response.status_code == 204:
        print(f"Entity {entity_id} deleted successfully.")
    else:
        print(f"Failed to delete entity {entity_id}. Status code: {response.status_code}, Error: {response.text}")

def delete_all_trial_entities(workers):
    '''Deletes {
        urn:Building:facility001, 
        urn:Person:worker001, urn:Device:tracker001, 
        urn:Person:worker002, urn:Device:tracker002, 
        urn:Person:worker003, urn:Device:tracker003
        }'''
    delete_entity("urn:Building:facility001")
    for worker in workers:
        delete_entity(f"urn:Person:{worker['worker_id']}")
        delete_entity(f"urn:Device:{worker['device_id']}")

def delete_all_entities():
    '''Deletes all entities in the service path'''
    headers = {
        "Fiware-ServicePath": fiware_service_path
    }
    response = requests.get(orion_url, headers=headers)
    if response.status_code == 200:
        entities = response.json()
        for entity in entities:
            delete_entity(entity["id"])
    else:
        print(f"Failed to retrieve entities. Status code: {response.status_code}, Error: {response.text}")

def create_test_entity():

    test_entity = {
        "id": "test_entity",
        "type": "Test",
        "name": {
            "type": "Property",
            "value": "Test Entity"
        },
        "location": {
            "type": "GeoProperty",
            "value": {
                "type": "Point",
                "coordinates": [21.788930292, 38.288395556]
            }
        },
        "category": {
            "type": "Property",
            "value": ["test"]
        },
        "status": {
            "type": "Property",
            "value": "active"
        }
    }

    print("Entity defined, sending to Orion Context Broker...")
    # Define headers with service path
    headers_post = {
        "Content-Type": "application/json",
        "Fiware-ServicePath": fiware_service_path
    }

    # Create entity
    response = requests.post(orion_url, headers=headers_post, data=json.dumps(test_entity))
    if response.status_code == 201:
        print(f"Entity {test_entity['id']} created successfully.")
    else:
        print(f"Failed to create entity {test_entity['id']}. Status code: {response.status_code}, Error: {response.text}")

    # Get entity to check if it was created
    headers = {
        "Fiware-ServicePath": fiware_service_path
    }
    response = requests.get(orion_url + "/test_entity", headers=headers)
    if response.status_code == 200:
        print(f"Entity {test_entity['id']} retrieved successfully.")
        print(response.json())
    else:
        raise Exception(f"Failed to retrieve entity {test_entity['id']}. Status code: {response.status_code}, Error: {response.text}")

    # define new service path
    new_headers = {
        "Content-Type": "application/json",
        "Fiware-ServicePath": "/ISAS/test2"
    }

    # create entity with new service path
    response = requests.post(orion_url, headers=new_headers, data=json.dumps(test_entity))
    if response.status_code == 201:
        print(f"Entity {test_entity['id']} created successfully.")
    else:
        raise Exception(f"Failed to create entity {test_entity['id']}. Status code: {response.status_code}, Error: {response.text}")
    
    # Get entity to check if it was created
    headers = {
        "Fiware-ServicePath": "/ISAS/test2"
    }
    response = requests.get(orion_url + "/test_entity", headers=headers)
    if response.status_code == 200:
        print(f"Entity {test_entity['id']} retrieved successfully.")
        print(response.json())
    else:
        raise Exception(f"Failed to retrieve entity {test_entity['id']}. Status code: {response.status_code}, Error: {response.text}")
    

    # Delete test entity
    input(f"Press Enter to delete the test entity in {fiware_service_path}...")
    headers = {
        "Fiware-ServicePath": fiware_service_path
    }
    response = requests.delete(orion_url + "/test_entity", headers=headers)
    if response.status_code == 204:
        print(f"Entity {test_entity['id']} deleted successfully.")
    else:
        raise Exception(f"Failed to delete entity {test_entity['id']}. Status code: {response.status_code}, Error: {response.text}")

    # Delete test entity with new service path
    input(f"Press Enter to delete the test entity in /ISAS/test2...")
    headers = {
        "Fiware-ServicePath": "/ISAS/test2"
    }
    response = requests.delete(orion_url + "/test_entity", headers=headers)
    if response.status_code == 204:
        print(f"Entity {test_entity['id']} deleted successfully.")
    else:
        raise Exception(f"Failed to delete entity {test_entity['id']}. Status code: {response.status_code}, Error: {response.text}")
    

def main_function():
    # Create a Building
    create_building()

    # Create 3 Worker (Person) Entities and their Devices
    workers = [
        {"worker_id": "worker001", "device_id": "tracker001", "location": [21.788930292, 38.288395556]},
        {"worker_id": "worker002", "device_id": "tracker002", "location": [21.789040292, 38.288395556]},
        {"worker_id": "worker003", "device_id": "tracker003", "location": [21.789150292, 38.288395556]}
    ]
    for worker in workers:
        create_device(worker["device_id"], worker["location"])
        create_person(worker["worker_id"], worker["device_id"], "urn:Building:facility001")

    # get worker002 current location
    headers = {
        "Fiware-ServicePath": fiware_service_path
    }
    response = requests.get(orion_url + "/urn:Person:worker002", headers=headers)
    if response.status_code == 200:
        print(f"Entity urn:Person:worker002 retrieved successfully.")
        print(response.json())
    else:
        print(f"Failed to retrieve entity urn:Person:worker002. Status code: {response.status_code}, Error: {response.text}")

    # update worker002 location
    new_location = [21.789250292, 38.288395556]
    update_entity = {
        "location": {
            "type": "geo:json",
            "value": {
                "type": "Point",
                "coordinates": new_location
            }
        }
    }
    headers = {
        "Content-Type": "application/json",
        "Fiware-ServicePath": fiware_service_path
    }
    response = requests.patch(orion_url + "/urn:Person:worker002/attrs", headers=headers, data=json.dumps(update_entity))
    if response.status_code == 204:
        print(f"Entity urn:Person:worker002 updated successfully.")
    else:
        print(f"Failed to update entity urn:Person:worker002. Status code: {response.status_code}, Error: {response.text}")
    
    # Delete the entities
    input("Press Enter to delete the entities...")
    delete_all_trial_entities(workers)
    print("All entities deleted successfully.")

# Main Function
def main():
    main_function()

    # check orion url and status
    # response = requests.get(orion_url)
    # print(response.status_code)
    # print(response.text)

    # Do test with Test Entity
    # create_test_entity()

if __name__ == "__main__":
    main()

import requests
import json

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
    with open("buildings.json") as f:
        entities = json.load(f) 
        for entity in entities:
            if entity["name"]["value"] == "R&D":
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
    with open("people.json") as f:
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

def post_device_entities():
    '''Post Device entities to the Context Broker'''
    with open("devices.json") as f:
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
    limit = 100
    response = requests.get(orion_url + "?limit=" + str(limit), headers=gd_headers)
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
    post_building_entities()
    post_person_entities()
    post_device_entities()
    userin = input("Press Enter to delete entities in the test path or type 'q' to exit: ")
    if userin == "q":
        return
    delete_in_path()

if __name__ == "__main__":
    main()
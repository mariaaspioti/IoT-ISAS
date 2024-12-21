import requests
import json

orion_url = "http://150.140.186.118:1026/v2/entities"
fiware_service = "ISAS"
fiware_service_path = "/test"
# PATCH headers
patch_headers = {
    "Content-Type": "application/json",
    "Fiware-Service": fiware_service,
    "Fiware-ServicePath": fiware_service_path
}
# GET/DELETE headers
gd_headers = {
    "Fiware-Service": fiware_service,
    "Fiware-ServicePath": fiware_service_path
}

def assign_devices():
    '''Assign devices entities to people entities, as they exist in the Context Broker
    
    - There exist Device entities in the Context Broker, that have
    controlledAsset attribute set to a Person entity.
    - There exist Person entities in the Context Broker, that have
    hasDevice attribute empty.
    - This function assigns Device entities to Person entities, by setting
    the hasDevice attribute of a Person entity to the id of the Device entity that
    controls the Person entity.'''

    # get all devices
    query = {
        "type": "Device",
        "limit": 1000
    }
    response = requests.get(orion_url, headers=gd_headers, params=query)
    devices = response.json()
    # print("Devices:")
    # print(devices)

    # get all people
    query = {
        "type": "Person",
        "limit": 1000
    }
    response = requests.get(orion_url, headers=gd_headers, params=query)
    people = response.json()
    # print("People:")
    # print(people)

    # assign devices to people
    for device in devices:
        if "controlledAsset" in device:
            person_id = device["controlledAsset"]["value"][0]
            for person in people:
                if person["id"] == person_id:
                    # check if person hasDevices attribute is empty, if not keep it and add the new device
                    if "hasDevices" in person and person["hasDevices"]["value"]:
                        person["hasDevices"]["value"].append(device["id"])
                    else:
                        person["hasDevices"] = {
                            "type": "Relationship",
                            "value": [device["id"]]
                        }
                    payload = {
                        "hasDevices": person["hasDevices"]
                    }
                    print(f"payload: {payload}")
                    print(f"Assigning device {device['id']} to person {person['id']}")
                    userin = input("Continue? (y/n): ")
                    if userin == "y":
                        url = f"{orion_url}/{person['id']}/attrs"
                        response = requests.patch(url, headers=patch_headers, json=payload)
                        if response.status_code == 204:
                            print(f"Device {device['id']} assigned to person {person['id']}")
                        else:
                            print(f"Failed to assign device {device['id']} to person {person['id']} with status code {response.status_code}, response: {response.text}")


def main():
    assign_devices()

if __name__ == "__main__":
    main()
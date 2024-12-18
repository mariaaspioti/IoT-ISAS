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

def get_persons_building_name(id):
    # find Person 1's current building's name
    response = requests.get(orion_url + f"/urn:ngsi-ld:Person:{id}", headers=gd_headers)
    if not response.ok:
        print(f"Failed to retrieve entity urn:Person:{id} with status code {response.status_code}, response: {response.text}")
        return
    person = response.json()
    building_id = person["currentFacility"]["value"]
    response = requests.get(orion_url + "/" + building_id, headers=gd_headers)
    if not response.ok:
        print(f"Failed to retrieve entity {building_id} with status code {response.status_code}, response: {response.text}")
        return
    building = response.json()
    print(f"Person {id} is in building {building['name']['value']}")

def get_location_of_all_cleanroom_operators():
    # find all cleanroom operators' locations
    response = requests.get(orion_url + "?type=Person", headers=gd_headers)
    if not response.ok:
        print(f"Failed to retrieve entities with status code {response.status_code}, response: {response.text}")
        return
    persons = response.json()
    for person in persons:
        if "Cleanroom Operator" in person["role"]["value"]:
            building_id = person["currentFacility"]["value"]
            response = requests.get(orion_url + "/" + building_id, headers=gd_headers)
            if not response.ok:
                print(f"Failed to retrieve entity {building_id} with status code {response.status_code}, response: {response.text}")
                return
            building = response.json()
            print(f"{person['name']['value']} is in building {building['name']['value']}")

def main():
    # get_persons_building_name(1)
    get_location_of_all_cleanroom_operators()

if __name__ == "__main__":
    main()
import requests
import json

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

# Query to get all devices with name starting with SmartLock-
query_params = {
    'type': 'Device',
    'q': 'name~=^SmartLock-',
    'limit': 1000
}

# Get the list of entities
response = requests.get(orion_url, params=query_params, headers=gd_headers)

if response.status_code == 200:
    entities = response.json()
    for entity in entities:
        entity_id = entity['id']
        
        # Check if the entity already has the hardLock attribute
        if 'hardLock' in entity:
            print(f'Entity {entity_id} already has the hardLock attribute')
            continue
        
        # Add the hardLock attribute
        update_url = f'{orion_url}/{entity_id}/attrs'
        payload = {
            'hardLock': {
                'type': 'Boolean',
                'value': False,

            }
        }
        update_response = requests.post(update_url, data=json.dumps(payload), headers=pp_headers)
        if update_response.status_code == 204:
            print(f'Successfully added hardLock to entity {entity_id}')
        else:
            print(f'Failed to add hardLock to entity {entity_id}: {update_response.status_code}')
else:
    print(f'Failed to retrieve entities: {response.status_code}')
import json
from faker import Faker

import data as mydata

fake = Faker()

def generate_building_entities(data):
    '''Generate Building entities based on the Building Smart Data Model
    https://github.com/smart-data-models/dataModel.Building/blob/master/Building/doc/spec.md
    Required fields:
    - id: unique identifier
    - type: entity type
    - address: the address of the building
    - category: the category of the building, Enum:'apartments, bakehouse, barn, bridge, bungalow,
         bunker, cathedral, cabin, carport, chapel, church, civic, commercial, conservatory, 
         construction, cowshed, detached, digester, dormitory, farm, farm_auxiliary, garage, 
         garages, garbage_shed, grandstand, greenhouse, hangar, hospital, hotel, house, houseboat,
         hut, industrial, kindergarten, kiosk, mosque, office, parking, pavilion, public, residential, 
         retail, riding_hall, roof, ruins, school, service, shed, shrine, stable, stadium, static_caravan, 
         sty, synagogue, temple, terrace, train_station, transformer_tower, transportation, university, 
         warehouse, water_tower'
    
    Purpose: to generate Building entities for the semiconductor manufacturing site,
     based on INTEL's Collinstown Industrial Park in Leixlip, Ireland'''

    entities = []
    for building in data:
        entity = {
            "id": f"{building['id']}",
            "type": "Building",
            "address": {
                "type": "StructuredValue",
                "value": {
                    "addressCountry": "IE",
                    "addressLocality": "Leixlip",
                    "addressRegion": "Kildare",
                    "postalCode": "W23",
                    "streetAddress": "Collinstown Industrial Park"
                }
            },
            "name": {
                "type": "Text",
                "value": building['name']
            },
            "description": {
                "type": "Text",
                "value": building['description']
            },
            "category": {
                "type": "Text",
                "value": building['category']
            },
            "location": {
                "type": "geo:json",
                "value": {
                    "type": "Polygon",
                    "coordinates": building['coordinates']
                }
            },
            "peopleCapacity": {
                "type": "Number",
                "value": building['peopleCapacity']
            },
            "peopleOccupancy": {
                "type": "Number",
                "value": building['peopleOccupancy']
            }
        }
        if "cleanrooms" in building:
            entity["cleanrooms"] = {
                "type": "Relationship",
                "value": building["cleanrooms"]
            }
        if "partOf" in building:
            entity["partOf"] = {
                "type": "Relationship",
                "value": building["partOf"]
            }
        entities.append(entity)
    return entities

def json_one_building(data):
    '''Generate a single Building entity based on the Building Smart Data Model'''
    
    entities = generate_building_entities([data])
    with open("buildings.json", "w") as f:
        json.dump(entities, f, indent=2)

def make_buildings_json(data):
    '''Generate Building entities based on the Building Smart Data Model'''
    
    entities = generate_building_entities(data)
    with open("buildings.json", "w") as f:
        json.dump(entities, f, indent=2)

def generate_person_entities(data):
    '''Generate Person entities based on the Person Smart Data Model
    https://github.com/smart-data-models/dataModel.Organization/blob/master/Person/doc/spec.md
    Required fields: 
    - id: unique identifier
    - type: entity type

    Purpose: to generate Person entities for the semiconductor manufacturing site,
     representing the workers'''
    
    entities = []
    for person in data:
        entity = {
            "id": f"{person['id']}",
            "type": "Person",
            "name": {
                "type": "Text",
                "value": person['name']
            },
            "hasDevices": {
                "type": "Relationship",
                "value": person['hasDevices']
            },
            "currentFacility": {
                "type": "Relationship",
                "value": person['currentFacility']
            },
            "role": {
                "type": "Text",
                "value": person['role']
            }
        }
        entities.append(entity)
    return entities

def make_person_json(data):
    '''Generate Person entities based on the Person Smart Data Model'''
    
    entities = generate_person_entities(data)
    with open("people.json", "w") as f:
        json.dump(entities, f, indent=2)


def generate_device_entities(data):
    '''Generate Device entities based on the Device Smart Data Model
    https://github.com/smart-data-models/dataModel.Device/blob/master/Device/doc/spec.md
    Required fields:
    - id: unique identifier
    - type: entity type
    - controlledProperty: the property or 'reading' that the device controls

    Purpose: to generate Device entities for the semiconductor manufacturing site,
     representing the environmental sensors, cameras, tracking devices, SOS buttons for each worker.'''
    
    entities = []
    for device in data:
        entity = {
            "id": f"{device['id']}",
            "type": "Device",
            "name": {
                "type": "Text",
                "value": device['name']
            },
            "description": {
                "type": "Text",
                "value": device['description']
            },
            "deviceCategory": {
                "type": "StructuredValue",
                "value": device['deviceCategory']
            },
            "controlledProperty": {
                "type": "StructuredValue",
                "value": device['controlledProperty']
            },
            "controlledAsset": {
                "type": "StructuredValue",
                "value": device['controlledAsset']
            },
            "supportedProtocol": { 
                "type": "StructuredValue",
                "value": device['supportedProtocol']
            },
            "location": {
                "type": "geo:json",
                "value": {
                    "type": "Point",
                    "coordinates": device['coordinates']
                }
            },
            "rssi" : {
                "type": "Number",
                "value": device['rssi']
            },
            "batteryLevel": {
                "type": "Number",
                "value": device['batteryLevel']
            },
            "dateLastValueReported": {
                "type": "DateTime",
                "value": device['dateLastValueReported']
            }
        }
        entities.append(entity)
    return entities

def make_device_json(data):
    '''Generate Device entities based on the Device Smart Data Model'''
    
    entities = generate_device_entities(data)
    with open("devices.json", "w") as f:
        json.dump(entities, f, indent=2)

def main():
    # make_buildings_json(mydata.building_data)
    # make_person_json(mydata.person_data)
    make_device_json(mydata.device_data)


if __name__ == "__main__":
    main()
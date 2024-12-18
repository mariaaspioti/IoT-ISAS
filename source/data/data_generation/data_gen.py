from faker import Faker
import json

fake = Faker()

def generate_test_entities():
    entities = []
    for i in range(10):
        entity = {
            "id": "urn:Device:" + str(i),
            "type": "Device",
            "temperature": {
                "value": fake.random_int(0, 100),
                "type": "Float"
            },
            "pressure": {
                "value": fake.random_int(0, 100),
                "type": "Float"
            },
            "humidity": {
                "value": fake.random_int(0, 100),
                "type": "Float"
            },
            "dateObserved": {
                "value": fake.date_time_this_month().isoformat(),
                "type": "DateTime"
            }
        }
        entities.append(entity)
    return entities

def do_test():
    test_file = "test.json"
    entities = generate_test_entities()
    with open(test_file, "w") as f:
        json.dump(entities, f, indent=2)

def generate_Person_entities():
    entities = []

    # TODO
    worker_id =...
    device_id =...
    building_id =...
    for i in range(10):
        entity = {
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
        entities.append(entity)
    return entities

def generate_Device_BTtracker_entities(num: int):
    ''' Generate Device entities based on the Device Smart Data Model
    https://github.com/smart-data-models/dataModel.Device/blob/master/Device/doc/spec.md
    Required fields:
    - id: unique identifier
    - type: entity type
    - controlledProperty: the property, reading, or measurement that the device controls
    
    Purpose: to generate Device entities for a Bluetooth tracker device that
        tracks the Person's who is carrying the device location'''
    entities = []
    for i in range(num):
        entity = {
            "id": f"urn:Device:{i}",
            "type": "Device",
            "controlledProperty": {
                "type": "Text",
                "value": "Location"
            },
            "location": {
                "type": "geo:json",
                "value": {
                    "type": "Point",
                    "coordinates": f"[{fake.longitude()}, {fake.latitude()}]"
                }
            }
        }
        entities.append(entity)
    return entities

def do_BTtrackers():
    file = "BTtrackers.json"
    entities = generate_Device_BTtracker_entities(10)
    with open(file, "w") as f:
        json.dump(entities, f, indent=2)

def main():
    # do_test()
    do_BTtrackers()


if __name__ == "__main__":
    main()


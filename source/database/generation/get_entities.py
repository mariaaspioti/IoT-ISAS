import requests
import csv
import os
import json

def process_person(entity):
    # Add custom processing for person entities
    entity['processed'] = True
    return entity

def process_building(entity):
    # Add custom processing for building entities
    entity['processed'] = True
    return entity

def process_device(entity):
    # Add custom processing for device entities
    entity['processed'] = True
    return entity

def process_entity(entity):
    entity_type = entity['type']
    if entity_type == 'Person':
        return process_person(entity)
    elif entity_type == 'Building':
        return process_building(entity)
    elif entity_type == 'Device':
        return process_device(entity)
    else:
        return entity

def process_entities(entities):
    return [process_entity(entity) for entity in entities]


def fetch_entities(orion_url, headers):
    response = requests.get(orion_url, headers=headers)
    return response.json()

def save_entities_to_csv(entities, output_dir):
    schemas = {}
    for entity in entities:
        entity_type = entity['type']
        if entity_type not in schemas:
            schemas[entity_type] = []
        schemas[entity_type].append(entity)

    for entity_type, entities in schemas.items():
        csv_file = os.path.join(output_dir, f'{entity_type}.csv')
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            headers = entities[0].keys()
            writer.writerow(headers)
            for entity in entities:
                writer.writerow(entity.values())



def save_entities_to_json(entities, output_dir):
    json_file = os.path.join(output_dir, 'entities.json')
    with open(json_file, 'w') as file:
        json.dump(entities, file, indent=4)

def main():
    
    orion_url = "http://150.140.186.118:1026/v2/entities?limit=200"
    fiware_service = "ISAS"
    fiware_service_path = "/test"
    headers = {
        "Fiware-Service": fiware_service,
        "Fiware-ServicePath": fiware_service_path
    }

    entities = fetch_entities(orion_url, headers)
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'entities_csv')
    os.makedirs(output_dir, exist_ok=True)

    save_entities_to_csv(entities, output_dir)
    save_entities_to_json(entities, output_dir)

    print(f'Entities have been saved in {output_dir} directory.')
    
if __name__ == "__main__":
    main()
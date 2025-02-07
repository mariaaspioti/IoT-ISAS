import requests
import json
import csv
import os

def fetch_entities_from_context_broker(url, params=None, headers=None):
    """
    Fetch entities from a FIWARE Orion Context Broker using the NGSI v2 API.
    
    Args:
        url (str): The full URL to the entities endpoint (e.g., "http://localhost:1026/v2/entities").
        params (dict, optional): Query parameters to filter or limit results.
        headers (dict, optional): HTTP headers to include in the request.
    
    Returns:
        list: A list of entity dictionaries returned by the Context Broker.
    
    Raises:
        requests.HTTPError: If the HTTP request fails.
    """
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

def flatten_dict(d, parent_key='', sep='_'):
    """
    Recursively flattens a nested dictionary.

    For example:
        {"a": {"b": 1, "c": 2}, "d": 3}
    becomes:
        {"a_b": 1, "a_c": 2, "d": 3}

    Args:
        d (dict): The dictionary to flatten.
        parent_key (str): The prefix to use for keys (used in recursive calls).
        sep (str): Separator to use between keys.

    Returns:
        dict: A new flattened dictionary.
    """
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items

def flatten_entity(entity):
    """
    Flatten an NGSI entity by extracting the 'value' from each attribute.
    The 'id' and 'type' are included as-is.
    
    For each attribute:
      - If its 'value' is a list, join the items with a semicolon.
      - If its 'value' is a dictionary, flatten it recursively.
      - Otherwise, use the value directly.
    
    Args:
        entity (dict): An NGSI entity as returned by the Context Broker.
    
    Returns:
        dict: A flattened version of the entity.
    """
    flat = {}
    # Copy 'id' and 'type' directly.
    flat["id"] = entity.get("id", "")
    flat["type"] = entity.get("type", "")
    
    # Process every other key.
    for key, attribute in entity.items():
        if key in ["id", "type"]:
            continue

        # Get the attribute value.
        attr_value = attribute.get("value", None)

        if isinstance(attr_value, dict):
            # Recursively flatten the nested dictionary.
            flat.update(flatten_dict(attr_value, parent_key=key))
        elif isinstance(attr_value, list):
            # Optionally, if the list items are dictionaries and you want to flatten them,
            # you could iterate and flatten each. Here we simply join non-dict items.
            flat[key] = ";".join(map(str, attr_value))
        else:
            flat[key] = attr_value

    return flat

def save_entities_to_csv(entities, output_dir):
    """
    Group the provided entities by their 'type' and write each group to a CSV file.
    Each CSV file is named "<type>.csv" and stored in the given output directory.
    
    Args:
        entities (list): A list of entity dictionaries.
        output_dir (str): The directory in which to save the CSV files.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Group flattened entities by type.
    entities_by_type = {}
    for entity in entities:
        entity_type = entity.get("type", "Unknown")
        flat_entity = flatten_entity(entity)
        entities_by_type.setdefault(entity_type, []).append(flat_entity)
    
    # Write one CSV file per entity type.
    for entity_type, flattened_entities in entities_by_type.items():
        # Build a header containing all keys found among the entities.
        header_keys = set()
        for entity in flattened_entities:
            header_keys.update(entity.keys())
        header_keys = sorted(header_keys)  # Sort for consistency
        
        output_file = os.path.join(output_dir, f"{entity_type}.csv")
        with open(output_file, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header_keys)
            writer.writeheader()
            for row in flattened_entities:
                writer.writerow(row)
        print(f"Saved {len(flattened_entities)} '{entity_type}' entities to {output_file}")

def get_entities_and_save_csv(context_broker_url, output_dir, params=None, headers=None):
    """
    Retrieve entities from a FIWARE Orion Context Broker and save them as CSV files.
    
    This function will:
      1. Query the Context Broker at the provided URL.
      2. Flatten each NGSI entity (extracting the 'value' from each attribute).
      3. Group the entities by type and write each group to its own CSV file.
    
    Args:
        context_broker_url (str): The URL of the Context Broker's entities endpoint.
        output_dir (str): The directory where CSV files should be saved.
        params (dict, optional): Query parameters for the HTTP request.
        headers (dict, optional): HTTP headers for the request.
    """
    try:
        entities = fetch_entities_from_context_broker(context_broker_url, params=params, headers=headers)
        save_entities_to_csv(entities, output_dir)
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as ex:
        print(f"An error occurred: {ex}")

def main():
    orion_url = "http://150.140.186.118:1026/v2/entities"
    limit = 1000
    params = {"limit": limit}

    fiware_service = "ISAS"
    fiware_service_path = "/test"

    headers = {
        "Fiware-Service": fiware_service,
        "Fiware-ServicePath": fiware_service_path
    }

    output_dir = os.path.join(os.path.dirname(__file__), "../entities_csv")
    get_entities_and_save_csv(orion_url, output_dir, params=params, headers=headers)

if __name__ == "__main__":
    main()
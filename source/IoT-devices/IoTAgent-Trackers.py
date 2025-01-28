import random
import json
import datetime
import paho.mqtt.client as mqtt
import requests

# MQTT broker details
mqtt_broker = '150.140.186.118'
mqtt_port = 1883
client_id = "ISAS-BTtrackerSubscriber"
mqtt_base_topic = "ISAS/devices/BT/#"  # Subscribe to all topics

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

def query_device_id(device_id):
    """
    Query device ID from the Context Broker to check if it exists.
    """
    url = f"{orion_url}?q=name=={device_id}&attrs=id"
    response = requests.get(url, headers=gd_headers)
    if response.status_code == 200:
        res = response.json()
        if len(res) > 0:
            return res[0]["id"]
    return None

def patch_data_to_cb(data, cb_device_id):
    """
    Patch the location data to the Context Broker.
    """
    if cb_device_id is None:
        print(f"Device ID not found in Context Broker for: {data['device_id']}")
        return

    payload = {
        "location": {
            "type": "geo:json",
            "value": {
                "type": "Point",
                "coordinates": [data["lng"], data["lat"]]
            }
        },
        "dateLastValueReported": {
            "type": "DateTime",
            "value": datetime.datetime.now().isoformat()
        }
    }

    url = f"{orion_url}/{cb_device_id}/attrs"
    response = requests.patch(url, headers=pp_headers, json=payload)
    if response.status_code == 204:
        print(f"Data patched successfully for device ID: {cb_device_id}")
    else:
        print(f"Failed to patch data for device ID: {cb_device_id}. Response: {response.status_code}")

def on_message(client, userdata, message):
    """
    Callback function for MQTT. Processes incoming messages.
    """
    try:
        data = json.loads(message.payload.decode())
        print(f"Received data: {data}")
        # Query the device ID in the Context Broker
        cb_device_id = query_device_id(data["device_id"])
        # Patch the data to the Context Broker
        patch_data_to_cb(data, cb_device_id)

        # DEBUG: Print the data
        # print(f"Device ID: {data['device_id']}, Latitude: {data['lat']}, Longitude: {data['lng']}")

    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON message: {e}")
    except Exception as e:
        print(f"Error processing message: {e}")

def read_data_from_mqtt():
    """
    Read data from the MQTT broker and process messages.
    """
    print("Starting MQTT client...")
    client = mqtt.Client(client_id)
    client.connect(mqtt_broker, mqtt_port)
    client.on_message = on_message
    client.subscribe(mqtt_base_topic)
    print(f"Subscribed to topic: {mqtt_base_topic}")
    client.loop_forever()

def main():
    try:
        print("Initializing IoT Agent - Trackers...")
        read_data_from_mqtt()
    except KeyboardInterrupt:
        print("Shutting down IoT Agent - Trackers.")

if __name__ == "__main__":
    main()
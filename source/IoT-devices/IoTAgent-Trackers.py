import datetime
import json
import datetime
import paho.mqtt.client as mqtt
import requests

# MQTT broker details
mqtt_broker = '150.140.186.118'
mqtt_port = 1883
# client id is the base plus timestamp of execution
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
client_id = f"ISAS-BTtrackerSubscriber-{timestamp}"
print(f"Client ID: {client_id}")
mqtt_base_topic = "ISAS/devices/+/#"  # Listen to both BT and GPS topics

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
    Patch location data for both BT and GPS devices.
    """
    if not cb_device_id:
        print(f"Device {data['device_id']} not found in Context Broker")
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

    response = requests.patch(
        f"{orion_url}/{cb_device_id}/attrs",
        headers=pp_headers,
        json=payload
    )
    print(f"PATCH status: {response.status_code} for {cb_device_id}")

def on_message(client, userdata, message):
    """
    Handle incoming messages from both BT and GPS topics.
    """
    try:
        data = json.loads(message.payload.decode())
        print(f"Received from {message.topic}: {data}")
        cb_device_id = query_device_id(data["device_id"])
        patch_data_to_cb(data, cb_device_id)

        # Debug: print the device ID from the Context Broker
        # print(f"Patched data for Device ID: {cb_device_id}, Latitude: {data['lat']}, Longitude: {data['lng']}")
    except Exception as e:
        print(f"Error: {str(e)}")

def read_data_from_mqtt():
    client = mqtt.Client(client_id)
    client.connect(mqtt_broker, mqtt_port)
    client.on_message = on_message
    client.subscribe(mqtt_base_topic)
    print(f"Subscribed to {mqtt_base_topic}")
    client.loop_forever()

def main():
    try:
        print("Starting IoT Agent for BT/GPS trackers...")
        read_data_from_mqtt()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == "__main__":
    main()
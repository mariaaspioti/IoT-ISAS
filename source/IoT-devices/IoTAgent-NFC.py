import requests
import json
import datetime
import paho.mqtt.client as mqtt


# MQTT broker details
mqtt_broker = '150.140.186.118'
mqtt_port = 1883
# client id is the base plus timestamp of execution
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
client_id = f"ISAS-NFCReaderSubscriber-{timestamp}"
print(f"Client ID: {client_id}")

mqtt_nfc_topic = "ISAS/devices/NFC/#" # Listen to NFC topic

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
    ''' Patch data for NFC readers'''

    if not cb_device_id:
        print(f"Device {data['device_id']} not found in Context Broker")
        return

    payload = {
        "value": {
            "type": "Text",
            "value": data["uid"]
        },
        "dateLastValueReported": {
            "type": "DateTime",
            "value": data["timestamp"]
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
    Handle incoming messages from NFC reader topics.
    """
    try:
        data = json.loads(message.payload.decode())
        print(f"Received from {message.topic}: {data}")
        cb_device_id = query_device_id(data["device_id"])
        patch_data_to_cb(data, cb_device_id)

        
    except Exception as e:
        print(f"Error: {str(e)}")

def read_data_from_mqtt():
    client = mqtt.Client(client_id)
    client.connect(mqtt_broker, mqtt_port)
    client.on_message = on_message
    
    client.subscribe(mqtt_nfc_topic)
    print(f"Subscribed to {mqtt_nfc_topic}")
    
    client.loop_forever()


def main():
    try:
        print("Starting IoT Agent for NFC readers...")
        read_data_from_mqtt()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == "__main__":
    main()
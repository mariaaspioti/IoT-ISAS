import random
import json
import datetime
import paho.mqtt.client as mqtt
import requests

# MQTT broker details
mqtt_broker = '150.140.186.118'
mqtt_port = 1883
client_id = "KA_ISAS_2"
mqtt_topic = "ISAS/test"

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

def init_setup():
    ...

def query_device_id(device_id):
    '''Query device ID from Context Broker'''
    # print(f"Querying device ID: {device_id}")
    # TODO
    if device_id == "BluetoothTracker-0":
        cb_device_id = "urn:ngsi-ld:Device:0"
        return cb_device_id
    return None

def patch_data_to_cb(data, cb_device_id):
    '''Patch the location data to Context Broker'''
    # print(f"Patch data to Context Broker: {data}")
    # print(f"Device ID: {cb_device_id}")
    if cb_device_id is None:
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
        print(f"Failed to patch data for device ID: {cb_device_id}")

    # test validity
    response = requests.get(orion_url + f"/{cb_device_id}", headers=gd_headers)
    if response.status_code == 200:
        print(f"Data retrieved successfully for device ID: {cb_device_id}")
        res = response.json()
        print(f"Retrieved location: {res['location']}")
    else:
        print(f"Failed to retrieve data for device ID: {cb_device_id}")
    
    

def read_data_from_mqtt():
    '''Read data from MQTT broker'''
    print("Reading data from MQTT broker")
    client = mqtt.Client(client_id)
    client.connect(mqtt_broker, mqtt_port)

    def on_message(client, userdata, message):
        '''Callback function for MQTT'''
        data = json.loads(message.payload.decode())
        print(f"Received data: {data}")
        cb_device_id = query_device_id(data["device_id"])
        patch_data_to_cb(data, cb_device_id)

    client.on_message = on_message
    client.subscribe(mqtt_topic)
    client.loop_forever()

def main():
    init_setup()
    read_data_from_mqtt()

if __name__ == "__main__":
    main()
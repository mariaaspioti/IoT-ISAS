import datetime
import json
import paho.mqtt.client as mqtt
import requests

# Create a persistent HTTP session for efficiency
session = requests.Session()
# Update session headers for GET/DELETE requests 
session.headers.update({
    "Fiware-Service": "ISAS",
    "Fiware-ServicePath": "/test"
})

# MQTT broker details
mqtt_broker = '150.140.186.118'
mqtt_port = 1883
# Client ID is the base plus a timestamp of execution
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
client_id = f"ISAS-BTGPStrackerSubscriber-{timestamp}"
print(f"Client ID: {client_id}")

mqtt_bt_topic = "ISAS/devices/BT/#"  # Listen to BT topic
mqtt_gps_topic = "ISAS/devices/GPS/#"  # Listen to GPS topic

# Orion Context Broker details
orion_url = "http://150.140.186.118:1026/v2/entities"
fiware_service = "ISAS"
fiware_service_path = "/test"

# Headers for POST/PATCH requests
pp_headers = {
    "Content-Type": "application/json",
    "Fiware-Service": fiware_service,
    "Fiware-ServicePath": fiware_service_path
}

# (GET/DELETE headers are already in the session)

# In-memory cache for device IDs: maps device_id to the Context Broker's ID.
device_id_cache = {}

def query_device_id(device_id):
    """
    Query the Context Broker for a device's ID, using a cache for efficiency.
    """
    # Check if the device_id is already cached.
    if device_id in device_id_cache:
        return device_id_cache[device_id]

    url = f"{orion_url}?q=name=={device_id}&attrs=id"
    try:
        response = session.get(url)  # Reuse the session
        if response.status_code == 200:
            res = response.json()
            if res and len(res) > 0:
                cb_id = res[0]["id"]
                device_id_cache[device_id] = cb_id  # Cache the result
                return cb_id
    except Exception as e:
        print(f"Error in query_device_id: {e}")
    return None

def patch_data_to_cb(data, cb_device_id):
    """
    Patch location data for both BT and GPS devices to the Context Broker.
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

    try:
        patch_url = f"{orion_url}/{cb_device_id}/attrs"
        response = session.patch(patch_url, headers=pp_headers, json=payload)
        print(f"PATCH status: {response.status_code} for {cb_device_id}")
    except Exception as e:
        print(f"Error in patch_data_to_cb: {e}")

def on_message(client, userdata, message):
    """
    Handle incoming MQTT messages from BT and GPS topics.
    """
    try:
        data = json.loads(message.payload.decode())
        print(f"Received from {message.topic}")
        cb_device_id = query_device_id(data["device_id"])
        patch_data_to_cb(data, cb_device_id)
    except Exception as e:
        print(f"Error in on_message: {str(e)}")

def read_data_from_mqtt():
    client = mqtt.Client(client_id)
    client.connect(mqtt_broker, mqtt_port)
    client.on_message = on_message
    
    client.subscribe(mqtt_gps_topic)
    print(f"Subscribed to {mqtt_gps_topic}")
    client.subscribe(mqtt_bt_topic)
    print(f"Subscribed to {mqtt_bt_topic}")
    
    client.loop_forever()

def main():
    try:
        print("Starting IoT Agent for BT/GPS trackers...")
        read_data_from_mqtt()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == "__main__":
    main()



# import datetime
# import json
# import datetime
# import paho.mqtt.client as mqtt
# import requests

# # MQTT broker details
# mqtt_broker = '150.140.186.118'
# mqtt_port = 1883
# # client id is the base plus timestamp of execution
# timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
# client_id = f"ISAS-BTGPStrackerSubscriber-{timestamp}"
# print(f"Client ID: {client_id}")

# mqtt_bt_topic = "ISAS/devices/BT/#" # Listen to BT topic
# mqtt_gps_topic = "ISAS/devices/GPS/#" # Listen to GPS topic

# # Orion Context Broker details
# orion_url = "http://150.140.186.118:1026/v2/entities"
# fiware_service = "ISAS"
# fiware_service_path = "/test"
# # POST/PATCH headers
# pp_headers = {
#     "Content-Type": "application/json",
#     "Fiware-Service": fiware_service,
#     "Fiware-ServicePath": fiware_service_path
# }

# # GET/DELETE headers
# gd_headers = {
#     "Fiware-Service": fiware_service,
#     "Fiware-ServicePath": fiware_service_path
# }

# def query_device_id(device_id):
#     """
#     Query device ID from the Context Broker to check if it exists.
#     """
#     url = f"{orion_url}?q=name=={device_id}&attrs=id"
#     response = requests.get(url, headers=gd_headers)
#     if response.status_code == 200:
#         res = response.json()
#         if len(res) > 0:
#             return res[0]["id"]
#     return None

# def patch_data_to_cb(data, cb_device_id):
#     """
#     Patch location data for both BT and GPS devices.
#     """
#     if not cb_device_id:
#         print(f"Device {data['device_id']} not found in Context Broker")
#         return

#     payload = {
#         "location": {
#             "type": "geo:json",
#             "value": {
#                 "type": "Point",
#                 "coordinates": [data["lng"], data["lat"]]
#             }
#         },
#         "dateLastValueReported": {
#             "type": "DateTime",
#             "value": datetime.datetime.now().isoformat()
#         }
#     }

#     response = requests.patch(
#         f"{orion_url}/{cb_device_id}/attrs",
#         headers=pp_headers,
#         json=payload
#     )
#     print(f"PATCH status: {response.status_code} for {cb_device_id}")

# def on_message(client, userdata, message):
#     """
#     Handle incoming messages from both BT and GPS topics.
#     """
#     try:
#         data = json.loads(message.payload.decode())
#         print(f"Received from {message.topic}")#: {data}")
#         cb_device_id = query_device_id(data["device_id"])
#         patch_data_to_cb(data, cb_device_id)

#         # Debug: print the device ID from the Context Broker
#         # print(f"Patched data for Device ID: {cb_device_id}, Latitude: {data['lat']}, Longitude: {data['lng']}")
#     except Exception as e:
#         print(f"Error: {str(e)}")

# def read_data_from_mqtt():
#     client = mqtt.Client(client_id)
#     client.connect(mqtt_broker, mqtt_port)
#     client.on_message = on_message
    
#     client.subscribe(mqtt_gps_topic)
#     print(f"Subscribed to {mqtt_gps_topic}")
#     client.subscribe(mqtt_bt_topic)
#     print(f"Subscribed to {mqtt_bt_topic}")
    
#     client.loop_forever()

# def main():
#     try:
#         print("Starting IoT Agent for BT/GPS trackers...")
#         read_data_from_mqtt()
#     except KeyboardInterrupt:
#         print("Shutting down")

# if __name__ == "__main__":
#     main()
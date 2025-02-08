import datetime
import json
import paho.mqtt.client as mqtt
import requests
import threading
import time
import os
import sys

# Watchdog timer
last_activity_time = time.time()
watchdog_interval = 60  # 60 seconds
times_error_detected_connecting_to_mqtt = 0

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
        response = session.get(url, timeout=10) # Timeout after 10 seconds
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
        response = session.patch(patch_url, headers=pp_headers, json=payload, timeout=10)
        print(f"PATCH status: {response.status_code} for {cb_device_id}")
    except Exception as e:
        print(f"Error in patch_data_to_cb: {e}")

def on_message(client, userdata, message):
    """
    Handle incoming MQTT messages from BT and GPS topics.
    """
    global last_activity_time
    try:
        data = json.loads(message.payload.decode())
        print(f"Received from {message.topic}")
        cb_device_id = query_device_id(data["device_id"])
        patch_data_to_cb(data, cb_device_id)
        last_activity_time = time.time()  # Update the watchdog timer
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
    # client.loop_start() # Start the loop in a separate thread

global message_received

def watchdog_on_message(client, userdata, message):
    """
    A message was received, which means the agent is not listening to them.
    """
    global message_received
    message_received = True
    

def check_if_messages_are_published():
    """
    Check if messages are being published by querying the MQTT broker.
    """
    global times_error_detected_connecting_to_mqtt
    global message_received
    message_received = False
    try:
        client = mqtt.Client(client_id)
        client.connect(mqtt_broker, mqtt_port)
        client.on_message = watchdog_on_message
        client.loop_start()
        time.sleep(2)  # Wait for the connection to be established
        client.subscribe(mqtt_gps_topic)
        client.subscribe(mqtt_bt_topic)
        # Wait 10 seconds for messages to be published
        time.sleep(10)
        client.loop_stop()
        client.disconnect()
        if message_received:
            return True
        return False
    except Exception as e:
        print(f"Error in check_if_messages_are_published: {e}")
        times_error_detected_connecting_to_mqtt += 1
        return False


def watchdog():
    global last_activity_time
    while True:
        time.sleep(watchdog_interval)
        if time.time() - last_activity_time > watchdog_interval:
            res = check_if_messages_are_published()
            if res:
                print("Watchdog: Agent is frozen while messages are being published, restarting...")
                # Log the watchdog event
                with open("watchdog-trackers.log", "a") as log_file:
                    log_file.write(f"Watchdog triggered at {datetime.datetime.now()}\n")
                os.execv(sys.executable, ['python', f'"{sys.argv[0]}"'] + sys.argv[1:])
            else:
                if times_error_detected_connecting_to_mqtt > 3:
                    print("Watchdog: Error connecting to MQTT broker multiple times, shutting down...")
                    with open("watchdog-trackers.log", "a") as log_file:
                        log_file.write(f"Error connecting to MQTT broker multiple times at {datetime.datetime.now()}\n")
                    # Exit the program
                    os._exit(1)
                else:
                    print("Watchdog: Agent is active, but no messages are being published")
                    print("Continuing...")

def main():
    try:
        print("Starting IoT Agent for BT/GPS trackers...")
        threading.Thread(target=watchdog, daemon=True).start() # Start the watchdog thread
        read_data_from_mqtt()
        while True:
            pass # Keep the program running
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == "__main__":
    main()
from smartcard.System import readers
from smartcard.util import toHexString
import time
import datetime
import json
import paho.mqtt.client as mqtt
import requests
import numpy as np
import threading

route = np.array([ [ -6.525644638060893, 53.37593036842741],
                          [ -6.525558787099413, 53.37595597008681],
                          [ -6.525483667508107, 53.37596877091073],
                          [ -6.525381719491337, 53.37600717335942],
                          [ -6.525258308734205, 53.37602317436947],
                          [ -6.525188554827994, 53.376071177363606],
                          [ -6.525086606811224, 53.37610637952491],
                          [ -6.52506527964661, 53.37615438242526], 
                          [ -6.524984794370226, 53.37619918508342], 
                          [ -6.524909674778919, 53.376240787509516],
                          [ -6.524839920872708, 53.37629199043969],
                          [ -6.524829189502535, 53.37632079206085], # has reached door, wait for it to open
                          [ -6.524850626901632, 53.376410396979956],
                          [ -6.524904283752553, 53.37643919852104],
                          [ -6.525033060194803, 53.37646159970622],
                          [ -6.525140373896649, 53.376468000042664],
                          [ -6.525312075819628, 53.376474400378164],
                          [ -6.525607188499741, 53.37645199919972],
                          [ -6.525730599256874, 53.37647120021055],
                          [ -6.525843278643835, 53.37646159970622],
                          [ -6.52596668940097, 53.376532003354306],
                          [ -6.526009614881719, 53.37662160782902],
                          [ -6.526041808992277, 53.37669201121258],
                          [ -6.526036443307181, 53.37676881477102],
                          [ -6.526041808992277, 53.37683281763059],
                          [ -6.526057906047545, 53.37689682039398],
                          [ -6.526057906047545, 53.37698002384256], # has reached door, wait for it to open
                         ])

up_to_fab1 = [
  {
    "lat": 53.37593036842741,
    "lng": -6.525644638060893
  },
  {
    "lat": 53.37595597008681,
    "lng": -6.525558787099413
  },
  {
    "lat": 53.37596877091073,
    "lng": -6.525483667508107
  },
  {
    "lat": 53.37600717335942,
    "lng": -6.525381719491337
  },
  {
    "lat": 53.37602317436947,
    "lng": -6.525258308734205
  },
  {
    "lat": 53.376071177363606,
    "lng": -6.525188554827994
  },
  {
    "lat": 53.37610637952491,
    "lng": -6.525086606811224
  },
  {
    "lat": 53.37615438242526,
    "lng": -6.52506527964661
  },
  {
    "lat": 53.37619918508342,
    "lng": -6.524984794370226
  },
  {
    "lat": 53.376240787509516,
    "lng": -6.524909674778919
  },
  {
    "lat": 53.37629199043969,
    "lng": -6.524839920872708
  },
  {
    "lat": 53.37632079206085,
    "lng": -6.524829189502535
  }
]

fab1_to_cleanroom1 = [
  {
    "lat": 53.376410396979956,
    "lng": -6.524850626901632
  },
  {
    "lat": 53.37643919852104,
    "lng": -6.524904283752553
  },
  {
    "lat": 53.37646159970622,
    "lng": -6.525033060194803
  },
  {
    "lat": 53.376468000042664,
    "lng": -6.525140373896649
  },
  {
    "lat": 53.376474400378164,
    "lng": -6.525312075819628
  },
  {
    "lat": 53.37645199919972,
    "lng": -6.525607188499741
  },
  {
    "lat": 53.37647120021055,
    "lng": -6.525730599256874
  },
  {
    "lat": 53.37646159970622,
    "lng": -6.525843278643835
  },
  {
    "lat": 53.376532003354306,
    "lng": -6.52596668940097
  },
  {
    "lat": 53.37662160782902,
    "lng": -6.526009614881719
  },
  {
    "lat": 53.37669201121258,
    "lng": -6.526041808992277
  },
  {
    "lat": 53.37676881477102,
    "lng": -6.526036443307181
  },
  {
    "lat": 53.37683281763059,
    "lng": -6.526041808992277
  },
  {
    "lat": 53.37689682039398,
    "lng": -6.526057906047545
  },
  {
    "lat": 53.37698002384256,
    "lng": -6.526057906047545
  }
]



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

broker = '150.140.186.118'
port = 1883
# client id is the base plus timestamp of execution
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
client_id = f"ISAS-ScenarioPublisher-{timestamp}"
print(f"Client ID: {client_id}")
base_bt_topic = "ISAS/devices/BT"
base_gps_topic = "ISAS/devices/GPS"
base_nfc_reader_topic = "ISAS/devices/NFC"

person2_uid = '8CCF454F'
nfc_reader_1 = 'NFCReader-0'
smart_lock_1 = 'SmartLock-0'
smart_lock_1_id = 'urn:ngsi-ld:Device:91'
serial_number_1 = 67383352736
nfc_reader_2 = 'NFCReader-8'
smart_lock_2 = 'SmartLock-4'
smart_lock_2_id = 'urn:ngsi-ld:Device:95'
serial_number_2 = 45896483093
real_serial_number = 18043712356

# Function that reads NFC tags scanned in the NFC Reader device and publishes them to the MQTT Broker

def read_nfc_tags(mqtt_client, device_id, base_topic):
    last_uid = None

    while True:
        try:
            # List all connected readers
            reader_list = readers()
            if not reader_list:
                time.sleep(1)
                continue

            reader = reader_list[0]
            connection = reader.createConnection()
            connection.connect()

            # Send command to get the UID
            get_uid_command = [0xFF, 0xCA, 0x00, 0x00, 0x00]
            response, sw1, sw2 = connection.transmit(get_uid_command)

            # Publish the UID if a card is detected
            if sw1 == 0x90 and sw2 == 0x00:
                uid = toHexString(response)
                uid = uid.replace(" ", "")
                if uid != last_uid:
                    payload = {
                        "device_id": device_id,
                        "uid": uid,
                        "timestamp": datetime.datetime.now().isoformat()
                    }
                    topic = f"{base_topic}/{device_id}"
                    mqtt_client.publish(topic, json.dumps(payload))
                    print(f"Published to {topic}: {payload}")
                    last_uid = uid
                    break  # Exit the loop after publishing the tag
            else:
                last_uid = None

        except Exception as e:
            last_uid = None
            time.sleep(1)



def change_device_serial_number(device_id, new_serial_number):
    command_url = f"{orion_url}/{device_id}/attrs"
    command_payload = {
        "serialNumber": {
            "type": "Text",
            "value": new_serial_number
        }
    }
    try:
        response = requests.patch(command_url, headers=pp_headers, json=command_payload)
        if response.status_code == 204:
            print(f"Serial number for device {device_id} changed successfully to {new_serial_number}")
        else:
            print(f"Failed to change serial number for device {device_id}: {response.status_code}")
    except Exception as e:
        print(f"Error changing serial number for device {device_id}: {e}")

def restore_serial_number(device_id, old_serial_number):
    change_device_serial_number(device_id, old_serial_number)
    print(f"Serial number for device {device_id} restored to {old_serial_number}")


# Global lock and event to control NFC execution
nfc_lock = threading.Lock()
nfc_fab1_executed = threading.Event()
nfc_cleanroom1_executed = threading.Event()

def scenario_beacon(mqtt_client, route, device_id, base_topic, stop_event):
    i = 0
    while not stop_event.is_set():   
        if i == 27:
            restore_serial_number(smart_lock_2_id, serial_number_2)
            break
        
        payload = {"device_id": device_id, "lat": route[i][1], "lng": route[i][0]}
        topic = f"{base_topic}/{device_id}"
        mqtt_client.publish(topic, json.dumps(payload))
        print(f"{device_id} published to {topic}")

        # First NFC trigger condition (Fab 1)
        if (route[i][1] == 53.37632079206085 and route[i][0] == -6.524829189502535):
            with nfc_lock:
                if not nfc_fab1_executed.is_set():
                    print("Scan your NFC tag to unlock the door in Fab 1...")
                    change_device_serial_number(smart_lock_1_id, real_serial_number)
                    read_nfc_tags(mqtt_client, nfc_reader_1, base_nfc_reader_topic)
                    nfc_fab1_executed.set()

            time.sleep(13)  # No need to manually check stop_event here

        # Second NFC trigger condition (Cleanroom 1)
        if (route[i][1] == 53.37698002384256 and route[i][0] == -6.526057906047545):
            with nfc_lock:
                if not nfc_cleanroom1_executed.is_set():
                    print("Scan your NFC tag to unlock the door in Cleanroom 1...")
                    restore_serial_number(smart_lock_1_id, serial_number_1)
                    change_device_serial_number(smart_lock_2_id, real_serial_number)
                    read_nfc_tags(mqtt_client, nfc_reader_2, base_nfc_reader_topic)
                    nfc_cleanroom1_executed.set()

            time.sleep(5)  # No need to manually check stop_event here

        time.sleep(1.9)
        i += 1


def main():
    mqtt_client = mqtt.Client(client_id)
    mqtt_client.connect(broker, port)
    mqtt_client.loop_start()
    print("Connected to MQTT broker")

    i = 2
    clients = []
    threads = []
    stop_event = threading.Event()

    # Bluetooth device setup
    bt_device_id = f"BluetoothTracker-{i}"
    bt_unique_client_id = f"{client_id}-BT-{i}"
    bt_client = mqtt.Client(bt_unique_client_id)
    bt_client.connect(broker, port)
    bt_client.loop_start()
    clients.append(bt_client)

    bt_thread = threading.Thread(target=scenario_beacon, args=(bt_client, route, bt_device_id, base_bt_topic, stop_event))  
    threads.append(bt_thread)
    bt_thread.start()
    time.sleep(1 + np.random.uniform(0.5, 1.5))

    # GPS device setup
    gps_device_id = f"GPSTracker-{i}"
    gps_unique_client_id = f"{client_id}-GPS-{i}"
    gps_client = mqtt.Client(gps_unique_client_id)
    gps_client.connect(broker, port)
    gps_client.loop_start()
    clients.append(gps_client)

    gps_thread = threading.Thread(target=scenario_beacon, args=(gps_client, route, gps_device_id, base_gps_topic, stop_event))
    threads.append(gps_thread)
    gps_thread.start()
    time.sleep(1 + np.random.uniform(0.5, 1.5))

    # Graceful shutdown mechanism
    try:
        while any(thread.is_alive() for thread in threads):
            for thread in threads:
                thread.join(timeout=1)  # Check every second if threads are still running
            if stop_event.is_set():
                break  # Exit loop if stop_event is set
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected. Stopping execution...")
        stop_event.set()  # Signal all threads to stop
        for thread in threads:
            thread.join()  # Ensure threads stop before proceeding
        for client in clients:
            client.loop_stop()
            client.disconnect()
        print("All threads and clients stopped. Exiting program.")

if __name__ == "__main__":
    main()
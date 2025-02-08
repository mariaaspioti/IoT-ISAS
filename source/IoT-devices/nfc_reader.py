''' Script that reads NFC tags and sends the data to the MQTT Broker '''

from smartcard.System import readers
from smartcard.util import toHexString
import time
import datetime
import json
import threading
import paho.mqtt.client as mqtt

broker = '150.140.186.118'
port = 1883
# client id is the base plus timestamp of execution
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
client_id = f"ISAS-NFCReaderPublisher-{timestamp}"
print(f"Client ID: {client_id}")
base_nfc_reader_topic = "ISAS/devices/NFC"


# List of UIDs to mimic
uids = [
    "182C6B80",
    "8E546381",
    "152C2382",
    "1E2C2783",
    "5AB82C84",
    "35BC2209",
    "1E2C6B80",
]


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
            else:
                last_uid = None

        except Exception as e:
            last_uid = None
            time.sleep(1)

def mimic_read_nfc_tags(mqtt_client, device_id, base_topic):
    '''Mimic reading NFC tags and sending the data to the MQTT Broker'''

    while True:
        try:
            for uid in uids:
                payload = {
                    "device_id": device_id,
                    "uid": uid,
                    "timestamp": datetime.datetime.now().isoformat()
                }
                topic = f"{base_topic}/{device_id}"
                mqtt_client.publish(topic, json.dumps(payload))
                print(f"Published to {topic}: {payload}")
                time.sleep(5)

        except Exception as e:
            time.sleep(1)


def start_mimic_reader(device_id, interval, mqtt_client ):
        threading.Thread(target=mimic_read_nfc_tags, args=(mqtt_client, device_id, base_nfc_reader_topic), daemon=True).start()
        time.sleep(interval)

def main():
    mqtt_client = mqtt.Client(client_id)
    mqtt_client.connect(broker, port)
    mqtt_client.loop_start()
    i=0
    print("Connected to MQTT broker")

    nfc_device_id = f"NFCReader-{i}"
    

    # Start mimic readers
    # start_mimic_reader("NFCReader-1", 3, mqtt_client)
    # start_mimic_reader("NFCReader-2", 3, mqtt_client)
    try:
        read_nfc_tags(mqtt_client, nfc_device_id, base_nfc_reader_topic)
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        print("Disconnected from MQTT broker")

if __name__ == "__main__":
    main()
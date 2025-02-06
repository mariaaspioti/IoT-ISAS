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
client_id = f"ISAS-SOSButtonSubscriber-{timestamp}"
print(f"Client ID: {client_id}")

mqtt_base_topic = "ISAS/devices/SOSButton/#" # Listen to SOSButton topic
mqtt_aux_topic = "json/Buttons/#" # Listen for real button presses

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

def compile_alert_data(data):
    ''' Compile the data from the SOS button press into a format suitable for the Alert entity. '''
    def query_id():
        # Query the last ID of the Alert entities from the Context Broker
        url = f"{orion_url}?type=Alert&limit=1&orderBy=!dateCreated"
        response = requests.get(url, headers=gd_headers)
        if response.status_code == 200:
            res = response.json()
            # if there are any entities, return the ID of the first one
            if len(res) > 0:
                return res[0]["id"]
            else:
                return False
            
    last_id = query_id()
    alert_id = f"urn:ngsi-ld:Alert:{int(last_id.split(':')[-1]) + 1}" if last_id else "urn:ngsi-ld:Alert:0"
    
    alert_data = {
        "id": alert_id,
        "sourceId": data["deviceInfo"]["deviceName"],
        # "dateIssued": data["time"],
        "category": "security",
        "subCategory": "suspiciousAction",
        "severity": "high",
        "name": "SOS Button Press Event",
        "description": "SOS button pressed by the worker",
        "status": "active"
    }
        
    return alert_data

def create_alert_entity(data):
    ''' Create an Alert entity for the SOS button press.
    Based on the Alert Smart Data Model
    https://github.com/smart-data-models/dataModel.Alert/blob/master/Alert/doc/spec.md '''

    entity = {
        "id": data["id"],
        "type": "Alert",
        "alertSource": {
            "type": "Relationship",
            "value": [
                data["sourceId"]
            ]
        },
        "category": {
            "type": "Text",
            "value": "security"
        },
        "dateIssued": {
            "type": "DateTime",
            "value": datetime.datetime.now().isoformat()
        },
        "subCategory": {
            "type": "Text",
            "value": data["subCategory"]
        },
        "severity": {
            "type": "Text",
            "value": data["severity"]
        },
        "name": {
            "type": "Text",
            "value": data["name"]
        },
        "description": {
            "type": "Text",
            "value": data["description"]
        },
        "status": {
            "type": "Text",
            "value": data["status"]
        }
    }
    print(f"Alert entity: {entity}")
    return entity

def post_entity_to_cb(entity):
    ''' Post Alert entity data to the Orion Context Broker. '''
    response = requests.post(
        orion_url,
        headers=pp_headers,
        json=entity
    )
    print(f"POST status: {response.status_code} for {entity['id']}")
    print(response.text)

def on_message(client, userdata, message):
    ''' Handle incoming messages sent by SOS buttons from the MQTT broker, and
     forward them to the Orion Context Broker. '''
    try:
        data = json.loads(message.payload.decode())
        print(f"Received from {message.topic}: {data}")
        alert_data = compile_alert_data(data)
        alert_entity = create_alert_entity(alert_data)
        post_entity_to_cb(alert_entity)

        # Debug: print the data from the Context Broker
    except Exception as e:
        print(f"Error: {str(e)}")

def read_data_from_mqtt():
    client = mqtt.Client(client_id)
    client.connect(mqtt_broker, mqtt_port)
    client.on_message = on_message
    
    client.subscribe(mqtt_aux_topic)
    print("Subscribed to topic:", mqtt_aux_topic)
    client.subscribe(mqtt_base_topic)
    print("Subscribed to topic:", mqtt_base_topic)

    client.loop_forever()

def main():
    try:
        print("Starting IoT Agent for SOS buttons...")
        read_data_from_mqtt()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == "__main__":
    main()
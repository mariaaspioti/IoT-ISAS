import json
import uuid
import paho.mqtt.client as mqtt
from datetime import datetime, timezone

broker = '150.140.186.118'
port = 1883
# client id is the base plus timestamp of execution
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
client_id = f"ISAS-SOSButtonPublisher-{timestamp}"
print(f"Client ID: {client_id}")
base_topic = "ISAS/devices/SOSButton"

def generate_button_press_message(
    # Optionally pass a device profile dictionary
    button_device=None,
    # Device-specific parameters (used only if button_device is not provided)
    tenantId="063a0ecb-e8c2-4a13-975a-93d791e8d40c",
    # tenantName="Smart Campus",
    applicationId="97865748-6f77-4f37-82f0-d76771651b21",
    # applicationName="Buttons",
    deviceProfileId="c707a935-359c-4359-9186-53bccc74bcb5",
    deviceProfileName="MClimate Multipurpose Button",
    deviceName="mclimate-multipurpose-button:0",
    devEui="70b3d52dd6000065",
    tags=None,
    
    # Message/sensor parameters
    temperature=20.0,
    pressEvent="01",
    batteryVoltage=3.4,
    thermistorProperlyConnected=True,
    
    # Radio and transmission parameters
    rssi=-100,
    snr=5.0,
    channel=1,
    frequency=868300000,
    spreadingFactor=7,
    
    # LoRaWAN transmission parameters
    fCnt=1,
    devAddr="0008b02d",
    dr=5,
    fPort=2,
    confirmed=True,
    data="",
    
    # Gateway information
    gatewayId="1dee04170f93c058"
):
    """
    Generate a LoRaWAN message with the provided custom values.
    If 'button_device' is provided, its contents are used as the device info.
    """
    # Create a unique deduplicationId using uuid4
    deduplicationId = str(uuid.uuid4())
    
    # Use current UTC time in ISO 8601 format
    now = datetime.now(timezone.utc).isoformat()

    # If a button_device dictionary is provided, use that for deviceInfo.
    # Otherwise, use the individual parameters.
    if button_device is not None:
        device_info = button_device
    else:
        # Default tags if not provided
        if tags is None:
            tags = {
                "deviceId": deviceName,
                "model": "multipurpose-button",
                "apiKey": "some-key",
                "manufacturer": "mclimate"
            }
        device_info = {
            "tenantId": tenantId,
            "tenantName": "Smart Campus",
            "applicationId": applicationId,
            "applicationName": "Buttons",
            "deviceProfileId": deviceProfileId,
            "deviceProfileName": deviceProfileName,
            "deviceName": deviceName,
            "devEui": devEui,
            "tags": tags
        }
    
    # If no custom data payload is provided, use a placeholder value.
    if not data:
        # Base64-encoded "Hello, World!"
        data = "SGVsbG8sIFdvcmxkIQ=="  # "Hello, World!"

    message = {
        "deduplicationId": deduplicationId,
        "time": now,
        "deviceInfo": device_info,
        "devAddr": devAddr,
        "adr": True,
        "dr": dr,
        "fCnt": fCnt,
        "fPort": fPort,
        "confirmed": confirmed,
        "data": data,
        "object": {
            "temperature": temperature,
            "pressEvent": pressEvent,
            "batteryVoltage": batteryVoltage,
            "thermistorProperlyConnected": thermistorProperlyConnected
        },
        "rxInfo": [
            {
                "gatewayId": gatewayId,
                "uplinkId": 10000,  # Example static value, adjust as needed
                "rssi": rssi,
                "snr": snr,
                "channel": channel,
                "location": {
                    "latitude": 38.288403977154466,
                    "longitude": 21.788731921156614
                },
                "context": "ExampleContext==",
                "metadata": {
                    "region_config_id": "eu868",
                    "region_common_name": "EU868"
                },
                "crcStatus": "CRC_OK"
            }
        ],
        "txInfo": {
            "frequency": frequency,
            "modulation": {
                "lora": {
                    "bandwidth": 125000,
                    "spreadingFactor": spreadingFactor,
                    "codeRate": "CR_4_5"
                }
            }
        }
    }

    return message

def generate_button_press_messages():
    # Define a default button_device dictionary
    default_button_device = {
        "tenantId": "063a0ecb-e8c2-4a13-975a-93d791e8d40c",
        "tenantName": "Smart Campus",
        "applicationId": "97865748-6f77-4f37-82f0-d76771651b21",
        "applicationName": "Buttons",
        "deviceProfileId": "c707a935-359c-4359-9186-53bccc74bcb5",
        "deviceProfileName": "MClimate Multipurpose Button",
        "deviceName": "mclimate-multipurpose-button:1",
        "devEui": "70b3d52dd6000065",
        "tags": {
            "deviceId": "mclimate-multipurpose-button:1",
            "model": "multipurpose-button",
            "apiKey": "some-key",
            "manufacturer": "mclimate"
        }
    }
    
    # Create a list to hold multiple messages
    messages = []
    
    # Message 1: Use the default button_device
    msg1 = generate_button_press_message(
        button_device=default_button_device,
        temperature=20.4,
        pressEvent="01",
        batteryVoltage=3.4,
        rssi=-112,
        snr=2.0,
        channel=7,
        frequency=867900000,
        spreadingFactor=7,
        fCnt=10
    )
    messages.append(msg1)
    
    # Message 2:
    button_device_button_2 = {
        "tenantId": "abc123-tenant",
        "applicationId": "app-456",
        "deviceProfileId": "profile-002",
        "deviceProfileName": "Example Button Model X",
        "deviceName": "mclimate-multipurpose-button:0",
        "devEui": "ABCDEF1234567890",
        "tags": {
            "deviceId": "mclimate-multipurpose-button:0",
            "model": "multipurpose-button",
            "apiKey": "custom-key-123",
            "manufacturer": "mclimate"
        }
    }
    msg2 = generate_button_press_message(
        button_device=button_device_button_2,
        temperature=19.9,
        pressEvent="01",
        batteryVoltage=3.6,
        rssi=-109,
        snr=4.0,
        channel=1,
        frequency=868300000,
        spreadingFactor=10,
        fCnt=9
    )
    messages.append(msg2)
    
    # Message 3: Using individual parameters (without button_device)
    # This will use the function's default device info
    # msg3 = generate_button_press_message(
    #     temperature=18.8,
    #     pressEvent="01",
    #     batteryVoltage=3.2,
    #     rssi=-113,
    #     snr=-7.5,
    #     channel=3,
    #     frequency=867100000,
    #     spreadingFactor=10,
    #     fCnt=8
    # )
    # messages.append(msg3)
    
    return messages

def transmit_messages(client, messages):
    '''Transmit the SOS button messages to the MQTT broker every time
    the user presses Enter.'''

    # Publish each message to the MQTT broker
    for i, message in enumerate(messages, start=1):
        # Wait for user input before sending the message
        userin = input("Press Enter to send the next SOS button message or 'q' to quit: ")
        if userin.lower() == 'q':
            break
        topic = f"{base_topic}/{message['deviceInfo']['deviceName']}"
        payload = json.dumps(message)
        client.publish(topic, payload)
        print(f"Published message {i} to topic {topic}")
        print(payload)
        print()

def main():
    # Create an MQTT client
    client = mqtt.Client(client_id)
    client.connect(broker, port)
    print("Connected to MQTT broker")
    
    # Generate button press messages
    messages = generate_button_press_messages()
    
    transmit_messages(client, messages)
    
    # Disconnect the client
    client.disconnect()
    print("Disconnected from MQTT broker")


if __name__ == "__main__":
    main()

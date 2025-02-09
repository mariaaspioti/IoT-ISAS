import json
import uuid
import paho.mqtt.client as mqtt
from datetime import datetime, timezone
from faker import Faker

# faker
fake = Faker()

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

def generate_sample_button_press_messages():
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

def create_button_device_message(id):
    button_device = {
        "tenantId": "063a0ecb-e8c2-4a13-975a-93d791e8d40c",
        "tenantName": "Smart Campus",
        "applicationId": "97865748-6f77-4f37-82f0-d76771651b21",
        "applicationName": "Buttons",
        "deviceProfileId": "c707a935-359c-4359-9186-53bccc74bcb5",
        "deviceProfileName": "MClimate Multipurpose Button",
        "deviceName": f"mclimate-multipurpose-button:{id}",
        "devEui": "70b3d52dd6000065",
        "tags": {
            "deviceId": f"mclimate-multipurpose-button:{id}",
            "model": "multipurpose-button",
            "apiKey": "some-key",
            "manufacturer": "mclimate"
        }
    }

    msg = generate_button_press_message(
        button_device=button_device,
        temperature=fake.pyfloat(min_value=18.0, max_value=22.0, right_digits=1),
        pressEvent="01",
        batteryVoltage=fake.pyfloat(min_value=3.2, max_value=3.6, right_digits=1),
        rssi=fake.random_int(min=-115, max=-60),
        snr=fake.pyfloat(min_value=1.0, max_value=10.0, right_digits=1),
        channel=fake.random_int(min=1, max=8),
        frequency=fake.random_int(min=867000000, max=868500000, step=100000),
        spreadingFactor=fake.random_int(min=7, max=12),
        fCnt=fake.random_int(min=1, max=100)
    )

    return msg


def transmit_message(message):
    '''Transmit the SOS button message to the MQTT broker every time
    the user presses Enter.'''

    # Publish the message to the MQTT broker
    # Wait for user input before sending the message
    userin = input("Press Enter to send the SOS button message or 'q' to quit: ")
    if userin.lower() == 'q':
        return False
    topic = f"{base_topic}/{message['deviceInfo']['deviceName']}"
    payload = json.dumps(message)
    # Create an MQTT client
    client = mqtt.Client(client_id)
    client.connect(broker, port)
    print("Connected to MQTT broker")
    client.publish(topic, payload)
    print(f"Published message to topic {topic}")
    print(payload)
    print()
    client.disconnect()
    print("Disconnected from MQTT broker")
    return True

def alt_main(id):
    # Generate button press messages
    button_message = create_button_device_message(id)
    print(f"Generated button press message for mclimate-multipurpose-button:{id}")
    print(json.dumps(button_message, indent=2))
    transmit_message(button_message)

def main():
    # Generate button press messages
    exit = False
    available_ids = range(0, 10)
    while not exit:
        print("===================")
        print(f"Available devices mclimate-multipurpose-button:{available_ids[0]} to mclimate-multipurpose-button:{available_ids[-1]}")
        print("Enter the ID of the device to simulate a button press, or 'q' to quit.")
        input_id = input(f"Device ID (0-{available_ids[-1]}): ")
        if input_id.lower() == 'q':
            exit = True
            break
        try:
            device_id = int(input_id)
            if device_id in available_ids:
                button_message = create_button_device_message(device_id)
                print(f"Generated button press message for mclimate-multipurpose-button:{device_id}")
                print(json.dumps(button_message, indent=2))
                transmit_message(button_message)
            else:
                print(f"Device ID {device_id} is not available.")
        except ValueError:
            print("Invalid input. Please enter a valid device ID.")
    print("Exiting...")
    print("Goodbye!")


if __name__ == "__main__":
    main()

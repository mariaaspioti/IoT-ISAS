'''
Start
  {
    "lat": 53.376431064762556,
    "lng": -6.528346538543702
  }
1.
  {
    "lat": 53.37647589103842,
    "lng": -6.52765989303589
  }
2.
  {
    "lat": 53.37693055488485,
    "lng": -6.5271878242492685
  }
- Retrace and repeat

'''

import time
import json
import numpy as np
import paho.mqtt.client as mqtt

broker = '150.140.186.118'
port = 1883
client_id = "ISAS-BTtrackerPublisher-0"
topic = "ISAS/test"

DEVICE_ID = "BluetoothTracker-0"

def get_parameters():
    route = np.array([ [-6.528346538543702, 53.376431064762556],
              [-6.52765989303589, 53.37647589103842],
              [-6.5271878242492685, 53.37693055488485],
              [-6.52765989303589, 53.37647589103842],
              [-6.528346538543702, 53.376431064762556] ])
    # time to complete motion, go from first point to last, then back to first
    total_time = 10

    # calculate the speed of the device
    speed = np.sum(np.linalg.norm(np.diff(route, axis=0), axis=1)) / total_time
    return route, speed

def main():
    route, speed = get_parameters()

    client = mqtt.Client(client_id)
    client.connect(broker, port)
    print("Connected to MQTT broker")

    start_time = time.time()
    direction = 1  # 1 for forward, -1 for reverse
    current_index = 0
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        # Calculate the total distance traveled
        total_distance = speed * elapsed_time

        # Calculate the distance between waypoints
        distances = np.linalg.norm(np.diff(route, axis=0), axis=1)
        cumulative_distances = np.cumsum(distances)

        # Find the current segment
        while current_index < len(cumulative_distances) and total_distance > cumulative_distances[current_index]:
            current_index += 1

        if current_index == len(cumulative_distances):
            direction *= -1
            current_index = 0
            start_time = current_time
            continue

        # Calculate the position between waypoints
        if current_index == 0:
            segment_start = route[0]
            segment_end = route[1]
            segment_distance = distances[0]
        else:
            segment_start = route[current_index]
            segment_end = route[current_index + 1]
            segment_distance = distances[current_index]

        segment_elapsed_distance = total_distance - (cumulative_distances[current_index - 1] if current_index > 0 else 0)
        segment_ratio = segment_elapsed_distance / segment_distance

        position = segment_start + segment_ratio * (segment_end - segment_start)

        # Publish the position to the MQTT broker
        payload = {"device_id": DEVICE_ID, "lat": position[1], "lng": position[0]}
        client.publish(topic, json.dumps(payload))
        print(f"Published data: {payload}")

        time.sleep(1)

if __name__=="__main__":
    main()
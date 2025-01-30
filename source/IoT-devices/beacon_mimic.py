'''
First
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

Second
  Start
  {
    "lat": 53.37424853336731,
    "lng": -6.523389816284181
  },
  {
    "lat": 53.374568736425694,
    "lng": -6.523271799087524
  },
  {
    "lat": 53.374850513125764,
    "lng": -6.523518562316895
  },
  {
    "lat": 53.37509386423014,
    "lng": -6.523518562316895
  },
  {
    "lat": 53.37478647313034,
    "lng": -6.522424221038818
  },
  {
    "lat": 53.3758046976512,
    "lng": -6.522252559661866
  },
  {
    "lat": 53.37617611940426,
    "lng": -6.523325443267823
  },
  {
    "lat": 53.37700220099962,
    "lng": -6.523507833480836
  }
  - Retrace and repeat  

'''

import time
import datetime
import json
import numpy as np
import paho.mqtt.client as mqtt
import threading

broker = '150.140.186.118'
port = 1883
# client id is the base plus timestamp of execution
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
client_id = f"ISAS-BTtrackerPublisher-{timestamp}"
print(f"Client ID: {client_id}")
base_topic = "ISAS/devices/BT"

def get_parameters():
    route_1 = np.array([ [-6.528346538543702, 53.376431064762556],
              [-6.52765989303589, 53.37647589103842],
              [-6.5271878242492685, 53.37693055488485], # End of route
              [-6.52765989303589, 53.37647589103842], # Retrace
              [-6.528346538543702, 53.376431064762556] ])
    route_2 = np.array([ [-6.523389816284181, 53.37424853336731],
              [-6.523271799087524, 53.374568736425694],
              [-6.523518562316895, 53.374850513125764],
              [-6.523518562316895, 53.37509386423014],
              [-6.522424221038818, 53.37478647313034],
              [-6.522252559661866, 53.3758046976512],
              [-6.523325443267823, 53.37617611940426],
              [-6.523507833480836, 53.37700220099962], # End of route
              [-6.523325443267823, 53.37617611940426], # Retrace
              [-6.522252559661866, 53.3758046976512],
              [-6.522424221038818, 53.37478647313034],
              [-6.523518562316895, 53.37509386423014],
              [-6.523518562316895, 53.374850513125764],
              [-6.523271799087524, 53.374568736425694],
              [-6.523389816284181, 53.37424853336731] ])
    
    total_time_1 = 30
    total_time_2 = 60

    speed_1 = np.sum(np.linalg.norm(np.diff(route_1, axis=0), axis=1)) / total_time_1
    speed_2 = np.sum(np.linalg.norm(np.diff(route_2, axis=0), axis=1)) / total_time_2

    routes = [route_1, route_2]
    speeds = [speed_1, speed_2]
    return routes, speeds
    

def mimic_beacon(mqtt_client, route, speed, device_id):
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
        payload = {"device_id": device_id, "lat": position[1], "lng": position[0]}
        topic = f"{base_topic}/{device_id}"
        mqtt_client.publish(topic, json.dumps(payload))
        print(f"{device_id} published: {payload}")

        time.sleep(1)

def main():
    bt_routes, speeds = get_parameters()

    client = mqtt.Client(client_id)
    client.connect(broker, port)
    print("Connected to MQTT broker")

    num_bt_devices = 2
    if len(bt_routes) < num_bt_devices:
        print(f"Number of routes ({len(bt_routes)}) is less than the number of devices ({num_bt_devices})")
        num_bt_devices = len(bt_routes)
    clients = []
    threads = []

    for i in range(num_bt_devices):
        device_id = f"BluetoothTracker-{i}"
        unique_client_id = f"{client_id}-{i}"
        client = mqtt.Client(unique_client_id)
        client.connect(broker, port)
        client.loop_start()  # Start MQTT network loop
        clients.append(client)
        thread = threading.Thread(target=mimic_beacon, args=(client, bt_routes[i], speeds[i], device_id))
        thread.daemon = True  # Thread exits when main thread exits
        threads.append(thread)
        thread.start()
        # delay between starting each thread
        time.sleep(1+np.random.rand())

    try:
        while True:  # Keep main thread alive
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        for client in clients:
            client.loop_stop()
            client.disconnect()
        print("Disconnected all clients.")


if __name__=="__main__":
    main()
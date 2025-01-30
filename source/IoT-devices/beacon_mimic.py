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
base_bt_topic = "ISAS/devices/BT"
base_gps_topic = "ISAS/devices/GPS"

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

def mimic_beacon(mqtt_client, route, speed, device_id, base_topic):
    start_time = time.time()
    current_index = 0
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        total_distance = speed * elapsed_time
        distances = np.linalg.norm(np.diff(route, axis=0), axis=1)
        cumulative_distances = np.cumsum(distances)

        while current_index < len(cumulative_distances) and total_distance > cumulative_distances[current_index]:
            current_index += 1

        if current_index == len(cumulative_distances):
            current_index = 0
            start_time = current_time
            continue

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

        payload = {"device_id": device_id, "lat": position[1], "lng": position[0]}
        topic = f"{base_topic}/{device_id}"
        mqtt_client.publish(topic, json.dumps(payload))
        print(f"{device_id} published to {topic}: {payload}")

        time.sleep(1)

def main():
    routes, speeds = get_parameters()

    client = mqtt.Client(client_id)
    client.connect(broker, port)
    print("Connected to MQTT broker")

    clients = []
    threads = []

    for i in range(len(routes)):
        route = routes[i]
        speed = speeds[i]

        # Bluetooth device setup
        bt_device_id = f"BluetoothTracker-{i}"
        bt_unique_client_id = f"{client_id}-BT-{i}"
        bt_client = mqtt.Client(bt_unique_client_id)
        bt_client.connect(broker, port)
        bt_client.loop_start()
        clients.append(bt_client)
        bt_thread = threading.Thread(target=mimic_beacon, args=(bt_client, route, speed, bt_device_id, base_bt_topic))
        bt_thread.daemon = True
        threads.append(bt_thread)
        bt_thread.start()
        time.sleep(1 + np.random.rand())

        # GPS device setup
        gps_device_id = f"GPSTracker-{i}"
        gps_unique_client_id = f"{client_id}-GPS-{i}"
        gps_client = mqtt.Client(gps_unique_client_id)
        gps_client.connect(broker, port)
        gps_client.loop_start()
        clients.append(gps_client)
        gps_thread = threading.Thread(target=mimic_beacon, args=(gps_client, route, speed, gps_device_id, base_gps_topic))
        gps_thread.daemon = True
        threads.append(gps_thread)
        gps_thread.start()
        time.sleep(1 + np.random.rand())

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        for client in clients:
            client.loop_stop()
            client.disconnect()
        print("Disconnected all clients.")

if __name__=="__main__":
    main()
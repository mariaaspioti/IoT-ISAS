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

Third
  Start
  {
    "lat": 53.37632097874124,
    "lng": -6.519856626052614
  },
  {
    "lat": 53.376090565227486,
    "lng": -6.520039059345767
  },
  {
    "lat": 53.375872951319856,
    "lng": -6.520200029898573
  },
  {
    "lat": 53.375706539934356,
    "lng": -6.520371731821533
  },
  {
    "lat": 53.375693739031604,
    "lng": -6.520693672927128
  },
  {
    "lat": 53.375770544390335,
    "lng": -6.5210692708836255
  },
  {
    "lat": 53.375936955525745,
    "lng": -6.520951225811587
  },
  {
    "lat": 53.376052162853995,
    "lng": -6.520704404297301
  },
  {
    "lat": 53.37603936205513,
    "lng": -6.520983419922144
  },
  {
    "lat": 53.37626337547967,
    "lng": -6.520543433744512
  },
  {
    "lat": 53.37600736004116,
    "lng": -6.520919031701031
  },
  {
    "lat": 53.37584734961057,
    "lng": -6.52117658458549
  },
  {
    "lat": 53.37621217251509,
    "lng": -6.521605839392929
  },
  {
    "lat": 53.37641058365992,
    "lng": -6.521841929537024
  },
  {
    "lat": 53.37685860542548,
    "lng": -6.522485811748172
  },
  {
    "lat": 53.37735782412665,
    "lng": -6.522872141074862
  },
  {
    "lat": 53.37766503272637,
    "lng": -6.523043842997841
  },
  {
    "lat": 53.37778663551822,
    "lng": -6.522292647084828
  },
  {
    "lat": 53.377658632569826,
    "lng": -6.522678976411517
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
client_id = f"ISAS-BTGPStrackerPublisher-{timestamp}"
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
    route_3 = np.array([ [-6.519856626052614, 53.37632097874124],
              [-6.520039059345767, 53.376090565227486],
              [-6.520200029898573, 53.375872951319856],
              [-6.520371731821533, 53.375706539934356],
              [-6.520693672927128, 53.375693739031604],
              [-6.5210692708836255, 53.375770544390335],
              [-6.520951225811587, 53.375936955525745],
              [-6.520704404297301, 53.376052162853995],
              [-6.520983419922144, 53.37603936205513],
              [-6.520543433744512, 53.37626337547967],
              [-6.520919031701031, 53.37600736004116],
              [-6.52117658458549, 53.37584734961057],
              [-6.521605839392929, 53.37621217251509],
              [-6.521841929537024, 53.37641058365992],
              [-6.522485811748172, 53.37685860542548],
              [-6.522872141074862, 53.37735782412665],
              [-6.523043842997841, 53.37766503272637],
              [-6.522292647084828, 53.37778663551822],
              [-6.522678976411517, 53.377658632569826], # End of route
              [-6.522292647084828, 53.37778663551822], # Retrace
              [-6.523043842997841, 53.37766503272637],
              [-6.522872141074862, 53.37735782412665],
              [-6.522485811748172, 53.37685860542548],
              [-6.521841929537024, 53.37641058365992],
              [-6.521605839392929, 53.37621217251509],
              [-6.52117658458549, 53.37584734961057],
              [-6.520919031701031, 53.37600736004116],
              [-6.520543433744512, 53.37626337547967],
              [-6.520983419922144, 53.37603936205513],
              [-6.520704404297301, 53.376052162853995],
              [-6.520951225811587, 53.375936955525745],
              [-6.5210692708836255, 53.375770544390335],
              [-6.520693672927128, 53.375693739031604],
              [-6.520371731821533, 53.375706539934356],
              [-6.520200029898573, 53.375872951319856],
              [-6.520039059345767, 53.376090565227486],
              [-6.519856626052614, 53.37632097874124] ])
    
    total_time_1 = 90
    total_time_2 = 120
    total_time_3 = 180

    speed_1 = np.sum(np.linalg.norm(np.diff(route_1, axis=0), axis=1)) / total_time_1
    speed_2 = np.sum(np.linalg.norm(np.diff(route_2, axis=0), axis=1)) / total_time_2
    speed_3 = np.sum(np.linalg.norm(np.diff(route_3, axis=0), axis=1)) / total_time_3

    routes = [route_1, route_2, route_3]
    speeds = [speed_1, speed_2, speed_3]
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
        print(f"{device_id} published to {topic}")#: {payload}")

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
        time.sleep(1 + np.random.uniform(0.5, 1.5)) # Random delay between devices

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
        time.sleep(1 + np.random.uniform(0.5, 1.5)) # Random delay between devices

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
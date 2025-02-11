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
base_nfc_reader_topic = "ISAS/devices/NFC"

door_cooldown = 4  # Cooldown time in seconds
last_door_trigger = {}  # Format: {(device_id, door_index): last_trigger_timestamp}
cooldown_lock = threading.Lock()  # Thread-safe access to last_door_trigger
device_at_door_index = {}  # key: device_id, value: current atDoorIndex


def get_door_parameters():
  door_locations = np.array([
      [-6.52482748, 53.376367338], 
      [-6.522874832, 53.376015129], 
      [-6.527380943, 53.376277685], 
      [-6.526683569, 53.377347103], 
      [-6.526007652, 53.376994902], 
      [-6.523604393, 53.375016122], 
      [-6.521619558, 53.374574246], 
      [-6.521984339, 53.374881638], 
      [-6.52233839, 53.375163614], 
      [-6.521083117, 53.374267052], 
      [-6.521093845, 53.37494588], 
      [-6.519141197, 53.374491195], 
      [-6.519334316, 53.374728144], 
      [-6.51976347, 53.375503022], 
      [-6.524634361, 53.375214846], 
      [-6.525557041, 53.374984303], 
      [-6.525900364, 53.37551583], 
      [-6.526694298, 53.37475376], 
      [-6.521018744, 53.375861639], 
      [-6.520332098, 53.37574637],
      [-6.521844864, 53.376591671], 
      [-6.522767544, 53.377726867], 
      [-6.523625851, 53.378378383], 
      [-6.528314352, 53.378160665]
  ])

  person_uids = ["1C553B4F", 
                 "9C72324F",
                 "8CCF454F",
                 "C23D4D41",
                 "182C6B80",
                 "8E546381",
                 "152C2382",
                 "1E2C2783",
                 "5AB82C84",
                 "35BC2209",
                 "1E2C6B80"]

  route_1_nfc_readers = [["NFCReader-4"],
                         ["NFCReader-6"], # last reader
                         ["NFCReader-7"], # Retrace, exit reader
                         ["NFCReader-5"]]
  
  routes_nfc_readers = [route_1_nfc_readers]
  return door_locations, person_uids, routes_nfc_readers

def check_door_proximity(door_locations, lat, lng):
    ''' This function checks if a device is close to a door. 
    Parameters:
      lat (float): The latitude of the device.
      lng (float): The longitude of the device.
    Returns:
      int: The index of the door the device is close to. -1 if the device is not close to any door.'''
    for i, door in enumerate(door_locations):
        if np.linalg.norm([lng, lat] - door) < 0.00007: # 0.00007 is approximately 5 meters
            return i
    return -1

def handle_door_entry(mqtt_client, lat, lng, device_id):
    door_locations, person_uids, routes_nfc_readers = get_door_parameters()
    # Determine if the device is physically close to a door.
    # (This returns the door’s physical index – used here only for logging and cooldown.)
    physical_door_index = check_door_proximity(door_locations, lat, lng)
    if physical_door_index == -1:
        return

    current_time = time.time()
    key = (device_id, physical_door_index)
    
    with cooldown_lock:
        # Enforce cooldown per (device, physical door) combination.
        last_trigger = last_door_trigger.get(key, 0)
        if current_time - last_trigger < door_cooldown:
            return  # Still in cooldown period
        last_door_trigger[key] = current_time

    # Log the door entry event.
    with open("door_entry.log", "a") as log_file:
        log_file.write(
            f"{device_id} is close to door {physical_door_index} at location {lat}, {lng} "
            f"-- {door_locations[physical_door_index][1]}, {door_locations[physical_door_index][0]} dat {datetime.datetime.now()}\n"
        )

    in_order_indexing = int(device_id.split("-")[-1])
    with cooldown_lock:
        # Get the current door count for this device (defaulting to 0 if not present).
        current_atDoorIndex = device_at_door_index.get(device_id, 0)
        # Get the NFC readers for this person's route, based on the in-order indexing
        # which stems from the device ID. i.e. 'BluetoothTracker-0' will use the first route.
        nfc_readers_for_person = routes_nfc_readers[in_order_indexing]
        # If the counter exceeds the number of NFC readers, reset it
        if current_atDoorIndex >= len(nfc_readers_for_person):
            current_atDoorIndex = 0

        # Retrieve the NFC reader name.
        # (In your data structure, each NFC reader is stored as a list with one item.
        # Adjust the indexing if your data structure changes.)
        nfc_reader_name = nfc_readers_for_person[current_atDoorIndex][0]

        # Increment and update the per-device counter for the next door event.
        device_at_door_index[device_id] = current_atDoorIndex + 1
    # -------------------------------------------------------------------------

    # Get the person's UID 
    person_uid = person_uids[in_order_indexing]

    # Create and publish the door entry event payload.
    payload = {
        "device_id": nfc_reader_name,
        "uid": person_uid,	
        "timestamp": datetime.datetime.now().isoformat()
    }
    topic = f"{base_nfc_reader_topic}/{nfc_reader_name}"
    mqtt_client.publish(topic, json.dumps(payload))
    # print(f"Published door entry for {device_id} to {topic} with payload: {payload}")
    with open("door_entry.log", "a") as log_file:
        log_file.write(f"Published door entry for {device_id} to {topic} with payload: {payload}\n")
    
def get_parameters():
    # route_1 = np.array([ [-6.528346538543702, 53.376431064762556],
    #           [-6.52765989303589, 53.37647589103842],
    #           [-6.5271878242492685, 53.37693055488485], # End of route
    #           [-6.52765989303589, 53.37647589103842], # Retrace
    #           [-6.528346538543702, 53.376431064762556] ])
    route_1 = np.array([ [-6.527753477659821, 53.37587935174477], 
                        [-6.527571044366648, 53.37600095963548], 
                        [-6.527388611073495, 53.376173770251256], 
                        [-6.527485193405168, 53.376416984004045], 
                        [-6.527935910952972, 53.376416984004045], 
                        [-6.527345685592745, 53.37658339261358], 
                        [-6.526648146530654, 53.37658339261358], 
                        [-6.526454981867309, 53.37665379606033], 
                        [-6.526358399535638, 53.3770442130619], 
                        [-6.526487175977868, 53.3773258231034], 
                        [-6.527034475857364, 53.37730022226749], 
                        [-6.527592507107033, 53.37702501230941], # End of route
                        [-6.527592507107033, 53.37702501230941], # Retrace
                        [-6.527034475857364, 53.37730022226749], 
                        [-6.526487175977868, 53.3773258231034], 
                        [-6.526358399535638, 53.3770442130619], 
                        [-6.526454981867309, 53.37665379606033], 
                        [-6.526648146530654, 53.37658339261358], 
                        [-6.527345685592745, 53.37658339261358], 
                        [-6.527935910952972, 53.376416984004045], 
                        [-6.527485193405168, 53.376416984004045], 
                        [-6.527388611073495, 53.376173770251256], 
                        [-6.527571044366648, 53.37600095963548], 
                        [-6.527753477659821, 53.37587935174477]])

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
    route_4 = np.array([ [-6.518441677804626, 53.375872737975605],
              [-6.518844104186584, 53.37547910999251],
              [-6.51919287371764, 53.3755975187928],
              [-6.519713345171654, 53.37555271550166],
              [-6.519809927503327, 53.3753863028649],
              [-6.519182142347447, 53.375181486419294],
              [-6.5191016646734425, 53.37492546447721],
              [-6.519906517437377, 53.37515268402765],
              [-6.519530919480881, 53.37478145145845],
              [-6.519139224469075, 53.37467584160187],
              [-6.519428971464113, 53.37444541918762],
              [-6.520072853675262, 53.37458623303334], # End of route
              [-6.519428971464113, 53.37444541918762], # Retrace
              [-6.519139224469075, 53.37467584160187],
              [-6.519530919480881, 53.37478145145845],
              [-6.519906517437377, 53.37515268402765],
              [-6.5191016646734425, 53.37492546447721],
              [-6.519182142347447, 53.375181486419294],
              [-6.519809927503327, 53.3753863028649],
              [-6.519713345171654, 53.37555271550166],
              [-6.51919287371764, 53.3755975187928],
              [-6.518844104186584, 53.37547910999251],
              [-6.518441677804626, 53.375872737975605] ])
    route_5 = np.array([ [-6.521043969187426, 53.3765287765295],
              [-6.521682485713479, 53.376695184702214],
              [-6.521848821951363, 53.37652237620217],
              [-6.522004426819073, 53.37630796468108],
              [-6.522374659090475, 53.37640076980034],
              [-6.522385390460666, 53.37626316213737],
              [-6.522685868825876, 53.37611595344752],
              [-6.5229648844507, 53.37602634790894],
              [-6.523372676517774, 53.376192758044844],
              [-6.523501452960004, 53.37637836858315],
              [-6.5241936263369995, 53.376493574717315], # End of route
              [-6.523501452960004, 53.37637836858315], # Retrace
              [-6.523372676517774, 53.376192758044844],
              [-6.5229648844507, 53.37602634790894],
              [-6.522685868825876, 53.37611595344752],
              [-6.522385390460666, 53.37626316213737],
              [-6.522374659090475, 53.37640076980034],
              [-6.522004426819073, 53.37630796468108],
              [-6.521848821951363, 53.37652237620217],
              [-6.521682485713479, 53.376695184702214],
              [-6.521043969187426, 53.3765287765295] ])
    route_6 = np.array([ [-6.525732487017282, 53.37492866476097],
              [-6.526038331067569, 53.37493506532779],
              [-6.526215398675644, 53.37481345439357],
              [-6.5268753779420825, 53.37496706814752],
              [-6.526349540802971, 53.37494466617623],
              [-6.5267036760191015, 53.37517188562423],
              [-6.526295883952048, 53.37552071312202], # End of route
              [-6.5267036760191015, 53.37517188562423], # Retrace
              [-6.526349540802971, 53.37494466617623],
              [-6.5268753779420825, 53.37496706814752],
              [-6.526215398675644, 53.37481345439357],
              [-6.526038331067569, 53.37493506532779],
              [-6.525732487017282, 53.37492866476097] ])
    route_7 = np.array([ [-6.525940572983141, 53.37682660402711],
              [-6.525951304353334, 53.377082614540846],
              [-6.525629363247758, 53.377082614540846],
              [-6.525597169137202, 53.37685860542548],
              [-6.525210839810492, 53.376877806252985],
              [-6.525382541733473, 53.376954609476364],
              [-6.524996212406782, 53.376935408683494],
              [-6.52498548103659, 53.377063413805686],
              [-6.525350347622914, 53.377185018315416],
              [-6.525457661324779, 53.377082614540846], # End of route
              [-6.525350347622914, 53.377185018315416], # Retrace
              [-6.525457661324779, 53.377082614540846],
              [-6.525350347622914, 53.377185018315416],
              [-6.52498548103659, 53.377063413805686],
              [-6.524996212406782, 53.376935408683494],
              [-6.525382541733473, 53.376954609476364],
              [-6.525210839810492, 53.376877806252985],
              [-6.525597169137202, 53.37685860542548],
              [-6.525629363247758, 53.377082614540846],
              [-6.525951304353334, 53.377082614540846],
              [-6.525940572983141, 53.37682660402711] ])
    route_8 = np.array([ [-6.523000177552201, 53.37572574128125],
              [-6.523064565773317, 53.37564893584171],
              [-6.523161148104989, 53.37554652837355],
              [-6.523225536326104, 53.375476123096355],
              [-6.522796281518665, 53.37538011571259],
              [-6.5225172658938195, 53.375239304491615],
              [-6.522742624667741, 53.37516889870653],
              [-6.523300655917411, 53.37532251117846],
              [-6.523043103032931, 53.3752713070827], # End of route
              [-6.523300655917411, 53.37532251117846], # Retrace
              [-6.522742624667741, 53.37516889870653],
              [-6.5225172658938195, 53.375239304491615],
              [-6.522796281518665, 53.37538011571259],
              [-6.523225536326104, 53.375476123096355],
              [-6.523161148104989, 53.37554652837355],
              [-6.523064565773317, 53.37564893584171],
              [-6.523000177552201, 53.37572574128125] ])
    route_9 = np.array([ [-6.526916494138468, 53.37779943579191],
              [-6.5277857351235395, 53.37789543772186],
              [-6.528633513368226, 53.37802984006022],
              [-6.52757110771981, 53.37803624016097],
              [-6.52752818223906, 53.37833704381217],
              [-6.52748525675833, 53.37803624016097],
              [-6.526787717696239, 53.3780042396475],
              [-6.526154566855263, 53.37804904035964],
              [-6.5249633847646376, 53.378183442213206],
              [-6.523911710486415, 53.37823464280776],
              [-6.523074663611902, 53.37823464280776],
              [-6.52380439678455, 53.37811304129519],
              [-6.52393317322678, 53.37851624497741],
              [-6.522988812650422, 53.37826024308196],
              [-6.522398587290195, 53.37859304524596],
              [-6.521883481521256, 53.37850984494877], # End of route
              [-6.522398587290195, 53.37859304524596], # Retrace
              [-6.522988812650422, 53.37826024308196],
              [-6.52393317322678, 53.37851624497741],
              [-6.52380439678455, 53.37811304129519],
              [-6.523074663611902, 53.37823464280776],
              [-6.523911710486415, 53.37823464280776],
              [-6.5249633847646376, 53.378183442213206],
              [-6.526154566855263, 53.37804904035964],
              [-6.526787717696239, 53.3780042396475],
              [-6.52748525675833, 53.37803624016097],
              [-6.52752818223906, 53.37833704381217],
              [-6.52757110771981, 53.37803624016097],
              [-6.528633513368226, 53.37802984006022],
              [-6.5277857351235395, 53.37789543772186],
              [-6.526916494138468, 53.37779943579191] ])
    route_10 = np.array([ [-6.525442625986566, 53.37530309630266],
              [-6.525555305373526, 53.375184686683816],
              [-6.5256250592797365, 53.37502467316239],
              [-6.525533842633161, 53.3749094630547],
              [-6.5253245809145275, 53.37493506532779],
              [-6.52486313199653, 53.37493506532779],
              [-6.524605579112071, 53.375040674541594],
              [-6.524519728150572, 53.375184686683816],
              [-6.524766549664859, 53.37525189218356],
              [-6.524991908438761, 53.37521028879149],
              [-6.525147513306451, 53.37513348242236],
              [-6.524970445698396, 53.37537030161554],
              [-6.525056296659876, 53.37545350804648],
              [-6.524830937885974, 53.37564872249634], # End of route
              [-6.525056296659876, 53.37545350804648], # Retrace
              [-6.524970445698396, 53.37537030161554],
              [-6.525147513306451, 53.37513348242236],
              [-6.524991908438761, 53.37521028879149],
              [-6.524766549664859, 53.37525189218356],
              [-6.524519728150572, 53.375184686683816],
              [-6.524605579112071, 53.375040674541594],
              [-6.52486313199653, 53.37493506532779],
              [-6.5253245809145275, 53.37493506532779],
              [-6.525533842633161, 53.3749094630547],
              [-6.5256250592797365, 53.37502467316239],
              [-6.525555305373526, 53.375184686683816],
              [-6.525442625986566, 53.37530309630266]
          ])
    route_11 = np.array([ [-6.520684304835045, 53.375098279456914],
                         [-6.5203838264698355, 53.375463108778035], # End of route
                         [-6.520684304835045, 53.375098279456914] ]) # Retrace
                  

    total_time_1 = 160
    total_time_2 = 120
    total_time_3 = 180
    total_time_4 = 150
    total_time_5 = 200
    total_time_6 = 120
    total_time_7 = 180
    total_time_8 = 220
    total_time_9 = 250
    total_time_10 = 180
    total_time_11 = 60

    speed_1 = np.sum(np.linalg.norm(np.diff(route_1, axis=0), axis=1)) / total_time_1
    speed_2 = np.sum(np.linalg.norm(np.diff(route_2, axis=0), axis=1)) / total_time_2
    speed_3 = np.sum(np.linalg.norm(np.diff(route_3, axis=0), axis=1)) / total_time_3
    speed_4 = np.sum(np.linalg.norm(np.diff(route_4, axis=0), axis=1)) / total_time_4
    speed_5 = np.sum(np.linalg.norm(np.diff(route_5, axis=0), axis=1)) / total_time_5
    speed_6 = np.sum(np.linalg.norm(np.diff(route_6, axis=0), axis=1)) / total_time_6
    speed_7 = np.sum(np.linalg.norm(np.diff(route_7, axis=0), axis=1)) / total_time_7
    speed_8 = np.sum(np.linalg.norm(np.diff(route_8, axis=0), axis=1)) / total_time_8
    speed_9 = np.sum(np.linalg.norm(np.diff(route_9, axis=0), axis=1)) / total_time_9
    speed_10 = np.sum(np.linalg.norm(np.diff(route_10, axis=0), axis=1)) / total_time_10
    speed_11 = np.sum(np.linalg.norm(np.diff(route_11, axis=0), axis=1)) / total_time_11

    routes = [route_1, route_2, route_3, route_4, route_5, route_6, route_7, route_8, route_9, route_10, route_11]
    speeds = [speed_1, speed_2, speed_3, speed_4, speed_5, speed_6, speed_7, speed_8, speed_9, speed_10, speed_11]
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
        if (device_id == "BluetoothTracker-0"):
            handle_door_entry(mqtt_client, position[1], position[0], device_id)
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
        print("...")
        print("...")
        print("...Stopping threads...")
        for client in clients:
            client.loop_stop()
            client.disconnect()
        print("Disconnected all clients.")

if __name__=="__main__":
    main()


'''
ROUTES
First
  Start
    {
    "lat": 53.37587935174477,
    "lng": -6.527753477659821
  },
  {
    "lat": 53.37600095963548,
    "lng": -6.527571044366648
  },
  {
    "lat": 53.376173770251256,
    "lng": -6.527388611073495
  },
  {
    "lat": 53.376416984004045,
    "lng": -6.527485193405168
  },
  {
    "lat": 53.376416984004045,
    "lng": -6.527935910952972
  },
  {
    "lat": 53.37658339261358,
    "lng": -6.527345685592745
  },
  {
    "lat": 53.37658339261358,
    "lng": -6.526648146530654
  },
  {
    "lat": 53.37665379606033,
    "lng": -6.526454981867309
  },
  {
    "lat": 53.3770442130619,
    "lng": -6.526358399535638
  },
  {
    "lat": 53.3773258231034,
    "lng": -6.526487175977868
  },
  {
    "lat": 53.37730022226749,
    "lng": -6.527034475857364
  },
  {
    "lat": 53.37702501230941,
    "lng": -6.527592507107033
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

Fourth
  Start
  {
    "lat": 53.375872737975605,
    "lng": -6.518441677804626
  },
  {
    "lat": 53.37547910999251,
    "lng": -6.518844104186584
  },
  {
    "lat": 53.3755975187928,
    "lng": -6.51919287371764
  },
  {
    "lat": 53.37555271550166,
    "lng": -6.519713345171654
  },
  {
    "lat": 53.3753863028649,
    "lng": -6.519809927503327
  },
  {
    "lat": 53.375181486419294,
    "lng": -6.519182142347447
  },
  {
    "lat": 53.37492546447721,
    "lng": -6.5191016646734425
  },
  {
    "lat": 53.37515268402765,
    "lng": -6.519906517437377
  },
  {
    "lat": 53.37478145145845,
    "lng": -6.519530919480881
  },
  {
    "lat": 53.37467584160187,
    "lng": -6.519139224469075
  },
  {
    "lat": 53.37444541918762,
    "lng": -6.519428971464113
  },
  {
    "lat": 53.37458623303334,
    "lng": -6.520072853675262
  }
  - Retrace and repeat

Fifth
  Start
  {
    "lat": 53.3765287765295,
    "lng": -6.521043969187426
  },
  {
    "lat": 53.376695184702214,
    "lng": -6.521682485713479
  },
  {
    "lat": 53.37652237620217,
    "lng": -6.521848821951363
  },
  {
    "lat": 53.37630796468108,
    "lng": -6.522004426819073
  },
  {
    "lat": 53.37640076980034,
    "lng": -6.522374659090475
  },
  {
    "lat": 53.37626316213737,
    "lng": -6.522385390460666
  },
  {
    "lat": 53.37611595344752,
    "lng": -6.522685868825876
  },
  {
    "lat": 53.37602634790894,
    "lng": -6.5229648844507
  },
  {
    "lat": 53.376192758044844,
    "lng": -6.523372676517774
  },
  {
    "lat": 53.37637836858315,
    "lng": -6.523501452960004
  },
  {
    "lat": 53.376493574717315,
    "lng": -6.5241936263369995
  }
  - Retrace and repeat

Sixth
 Start
 {
    "lat": 53.37492866476097,
    "lng": -6.525732487017282
  },
  {
    "lat": 53.37493506532779,
    "lng": -6.526038331067569
  },
  {
    "lat": 53.37481345439357,
    "lng": -6.526215398675644
  },
  {
    "lat": 53.37496706814752,
    "lng": -6.5268753779420825
  },
  {
    "lat": 53.37494466617623,
    "lng": -6.526349540802971
  },
  {
    "lat": 53.37517188562423,
    "lng": -6.5267036760191015
  },
  {
    "lat": 53.37552071312202,
    "lng": -6.526295883952048
  }
  - Retrace and repeat

Seventh
 Start
 {
    "lat": 53.37682660402711,
    "lng": -6.525940572983141
  },
  {
    "lat": 53.377082614540846,
    "lng": -6.525951304353334
  },
  {
    "lat": 53.377082614540846,
    "lng": -6.525629363247758
  },
  {
    "lat": 53.37685860542548,
    "lng": -6.525597169137202
  },
  {
    "lat": 53.376877806252985,
    "lng": -6.525210839810492
  },
  {
    "lat": 53.376954609476364,
    "lng": -6.525382541733473
  },
  {
    "lat": 53.376935408683494,
    "lng": -6.524996212406782
  },
  {
    "lat": 53.377063413805686,
    "lng": -6.52498548103659
  },
  {
    "lat": 53.377185018315416,
    "lng": -6.525350347622914
  },
  {
    "lat": 53.377082614540846,
    "lng": -6.525457661324779
  }
  - Retrace and repeat

Eighth
 Start
 {
    "lat": 53.37572574128125,
    "lng": -6.523000177552201
  },
  {
    "lat": 53.37564893584171,
    "lng": -6.523064565773317
  },
  {
    "lat": 53.37554652837355,
    "lng": -6.523161148104989
  },
  {
    "lat": 53.375476123096355,
    "lng": -6.523225536326104
  },
  {
    "lat": 53.37538011571259,
    "lng": -6.522796281518665
  },
  {
    "lat": 53.375239304491615,
    "lng": -6.5225172658938195
  },
  {
    "lat": 53.37516889870653,
    "lng": -6.522742624667741
  },
  {
    "lat": 53.37532251117846,
    "lng": -6.523300655917411
  },
  {
    "lat": 53.3752713070827,
    "lng": -6.523043103032931
  }
  - Retrace and repeat

Ninth
 Start
 {
    "lat": 53.37779943579191,
    "lng": -6.526916494138468
  },
  {
    "lat": 53.37789543772186,
    "lng": -6.5277857351235395
  },
  {
    "lat": 53.37802984006022,
    "lng": -6.528633513368226
  },
  {
    "lat": 53.37803624016097,
    "lng": -6.52757110771981
  },
  {
    "lat": 53.37833704381217,
    "lng": -6.52752818223906
  },
  {
    "lat": 53.37803624016097,
    "lng": -6.52748525675833
  },
  {
    "lat": 53.3780042396475,
    "lng": -6.526787717696239
  },
  {
    "lat": 53.37804904035964,
    "lng": -6.526154566855263
  },
  {
    "lat": 53.378183442213206,
    "lng": -6.5249633847646376
  },
  {
    "lat": 53.37823464280776,
    "lng": -6.523911710486415
  },
  {
    "lat": 53.37823464280776,
    "lng": -6.523074663611902
  },
  {
    "lat": 53.37811304129519,
    "lng": -6.52380439678455
  },
  {
    "lat": 53.37851624497741,
    "lng": -6.52393317322678
  },
  {
    "lat": 53.37826024308196,
    "lng": -6.522988812650422
  },
  {
    "lat": 53.37859304524596,
    "lng": -6.522398587290195
  },
  {
    "lat": 53.37850984494877,
    "lng": -6.521883481521256
  }
  - Retrace and repeat

Tenth
 Start
 {
    "lat": 53.37530309630266,
    "lng": -6.525442625986566
  },
  {
    "lat": 53.375184686683816,
    "lng": -6.525555305373526
  },
  {
    "lat": 53.37502467316239,
    "lng": -6.5256250592797365
  },
  {
    "lat": 53.3749094630547,
    "lng": -6.525533842633161
  },
  {
    "lat": 53.37493506532779,
    "lng": -6.5253245809145275
  },
  {
    "lat": 53.37493506532779,
    "lng": -6.52486313199653
  },
  {
    "lat": 53.375040674541594,
    "lng": -6.524605579112071
  },
  {
    "lat": 53.375184686683816,
    "lng": -6.524519728150572
  },
  {
    "lat": 53.37525189218356,
    "lng": -6.524766549664859
  },
  {
    "lat": 53.37521028879149,
    "lng": -6.524991908438761
  },
  {
    "lat": 53.37513348242236,
    "lng": -6.525147513306451
  },
  {
    "lat": 53.37537030161554,
    "lng": -6.524970445698396
  },
  {
    "lat": 53.37545350804648,
    "lng": -6.525056296659876
  },
  {
    "lat": 53.37564872249634,
    "lng": -6.524830937885974
  }
  - Retrace and repeat

Eleventh
  Start
  {
    "lat": 53.375098279456914,
    "lng": -6.520684304835045
  },
  {
    "lat": 53.375463108778035,
    "lng": -6.5203838264698355
  }
  - Retrace and repeat
'''
"""
DOOR LOCATIONS
[{"id":"urn:ngsi-ld:Door:0","type":"Door","location":{"type":"geo:json","value":{"type":"Point","coordinates":[-6.52482748,53.376367338]},"metadata":{}}},{"id":"urn:ngsi-ld:Door:1","type":"Door","location":{"type":"geo:json","value":{"type":"Point","coordinates":[-6.522874832,53.376015129]},"metadata":{}}},{"id":"urn:ngsi-ld:Door:2","type":"Door","location":{"type":"geo:json","value":{"type":"Point","coordinates":[-6.527380943,53.376277685]},"metadata":{}}},{"id":"urn:ngsi-ld:Door:3","type":"Door","location":{"type":"geo:json","value":{"type":"Point","coordinates":[-6.526683569,53.377347103]},"metadata":{}}},{"id":"urn:ngsi-ld:Door:4","type":"Door","location":{"type":"geo:json","value":{"type":"Point","coordinates":[-6.526007652,53.376994902]},"metadata":{}}},{"id":"urn:ngsi-ld:Door:5","type":"Door","location":{"type":"geo:json","value":{"type":"Point","coordinates":[-6.523604393,53.375016122]},"metadata":{}}},{"id":"urn:ngsi-ld:Door:6","type":"Door","location":{"type":"geo:json","value":{"type":"Point","coordinates":[-6.521619558,53.374574246]},"metadata":{}}},{"id":"urn:ngsi-ld:Door:7","type":"Door","location":{"type":"geo:json","value":{"type":"Point","coordinates":[-6.521984339,53.374881638]},"metadata":{}}},{"id":"urn:ngsi-ld:Door:8","type":"Door","location":{"type":"geo:json","value":{"type":"Point","coordinates":[-6.52233839,53.375163614]},"metadata":{}}},{"id":"urn:ngsi-ld:Door:9","type":"Door","location":{"type":"geo:json","value":{"type":"Point","coordinates":[-6.521083117,53.374267052]},"metadata":{}}},{"id":"urn:ngsi-ld:Door:10","type":"Door","location":{"type":"geo:json","value":{"type":"Point","coordinates":[-6.521093845,53.37494588]},"metadata":{}}},{"id":"urn:ngsi-ld:Door:11","type":"Door","location":{"type":"geo:json","value":{"type":"Point","coordinates":[-6.519141197,53.374491195]},"metadata":{}}},{"id":"urn:ngsi-ld:Door:12","type":"Door","location":{"type":"geo:json","value":{"type":"Point","coordinates":[-6.519334316,53.374728144]},"metadata":{}}},{"id":"urn:ngsi-ld:Door:13","type":"Door","location":{"type":"geo:json","value":{"type":"Point","coordinates":[-6.51976347,53.375503022]},"metadata":{}}},{"id":"urn:ngsi-ld:Door:14","type":"Door","location":{"type":"geo:json","value":{"type":"Point","coordinates":[-6.524634361,53.375214846]},"metadata":{}}},{"id":"urn:ngsi-ld:Door:15","type":"Door","location":{"type":"geo:json","value":{"type":"Point","coordinates":[-6.525557041,53.374984303]},"metadata":{}}},{"id":"urn:ngsi-ld:Door:16","type":"Door","location":{"type":"geo:json","value":{"type":"Point","coordinates":[-6.525900364,53.37551583]},"metadata":{}}},{"id":"urn:ngsi-ld:Door:17","type":"Door","location":{"type":"geo:json","value":{"type":"Point","coordinates":[-6.526694298,53.37475376]},"metadata":{}}},{"id":"urn:ngsi-ld:Door:18","type":"Door","location":{"type":"geo:json","value":{"type":"Point","coordinates":[-6.521018744,53.375861639]},"metadata":{}}},{"id":"urn:ngsi-ld:Door:19","type":"Door","location":{"type":"geo:json","value":{"type":"Point","coordinates":[-6.520332098,53.37574637]},"metadata":{}}}]
"""
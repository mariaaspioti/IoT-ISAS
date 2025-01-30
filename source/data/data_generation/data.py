# =============================================================================
# This file contains the data for the entities to be created in the context broker.
# The data is in the form of a list of dictionaries, where each dictionary represents an entity.
# =============================================================================

# =================== Building Data ===================
'''
0. REMF 
    Role: Likely the main manufacturing building area housing wafer fabrication processes, critical to producing semiconductor chips.

1. MANUFACTURING BUILDING FAB 1

    Role: One of the wafer fabrication facilities (FAB 1), where semiconductor wafers are processed into microchips. Contains CLEANROOM 1

2. MANUFACTURING BUILDING FAB 2

    Role: Similar to FAB 1, this building supports semiconductor manufacturing, a parallel fabrication line. Contains CLEANROOM 2

3. FAB 10

    Role: A fabrication facility, likely focusing on a specific set of processes, or more restricted possible output. Contains CLEANROOM 3

4. FAB 14

    Role: Another advanced fabrication plant where newer nodes or technologies might be utilized for chip production. Contains CLEANROOM 4

5. FAB 10 ENERGY CENTRE

    Role: Supports the FAB 10 operations with power and utilities such as electricity, cooling systems, and compressed gases.

6. FAB 14 ENERGY CENTRE

    Role: Provides essential utilities to FAB 14, including energy, HVAC (Heating, Ventilation, and Air Conditioning), and power backup systems.

7. R&D

    Role: Research and Development facility focused on process improvements, new node development, and innovation for advanced semiconductor technologies.

8. IR5

    Role: Office building that likely houses engineering teams, management, and other administrative staff supporting the manufacturing operations.

9. IR2

    Role: Similar to IR5, this is another office building for administrative, engineering, or support functions.

10. RODI

    Role: the Reverse Osmosis Deionized Water facility where ultrapure water is produced, essential for cleaning semiconductor wafers during fabrication.

11. ASU

    Role: Air Separation Units that generate critical gases like nitrogen, oxygen, and argon, which are used extensively in the manufacturing process.

12. Ryebrook 110kV Substation

    Role: A high-voltage power substation that distributes electricity across the site, ensuring a stable and sufficient power supply for energy-intensive operations.

13. Waste Water Treatment Building

    Role: Treats industrial wastewater generated during semiconductor production, ensuring environmental compliance and recycling wherever possible.

14. Water Treatment Building (Light Yellow)

    Role: Prepares ultrapure water and manages water treatment processes, a critical component for semiconductor fabrication.

15. MSCP 

    Role: Multi-Storey Car Park (MSCP) provides parking space for employees and visitors to the site.
'''

building_data = [
        {
            "id": "urn:ngsi-ld:Building:0",
            "name": "FAB 1",
            "description": "Semiconductor manufacturing site",
            "category": "industrial",
            "peopleCapacity": 300,
            "peopleOccupancy": 120,
            "coordinates": [
                [
                    [-6.526254415512086, 53.377564699115155],
                    [-6.523357629776002, 53.377660752805994],
                    [-6.523207426071167, 53.37632878896608],
                    [-6.522799730300904, 53.37610465634059],
                    [-6.5229177474975595, 53.37593815705524],
                    [-6.523454189300538, 53.37607263729782],
                    [-6.523550748825074, 53.37596377237229],
                    [-6.523722410202027, 53.37600219531896],
                    [-6.523507833480836, 53.376303173868585],
                    [-6.5239155292510995, 53.376277558755675],
                    [-6.523958444595338, 53.376380019114855],
                    [-6.52614712715149, 53.37632233395982],
                    [-6.526254415512086, 53.377564699115155]
                ]
            ],
            "cleanrooms": ["urn:ngsi-ld:Building:1"]
        },
        {
            "id": "urn:ngsi-ld:Building:1",
            "name": "Cleanroom 1",
            "description": "Wafer fabrication cleanroom",
            "category": "industrial",
            "peopleCapacity": 180,
            "peopleOccupancy": 125,
            "coordinates": [
                [
                    [-6.526050567626954, 53.377429875206566],
                    [-6.525986194610597, 53.37662941682359],
                    [-6.524022817611695, 53.37671266519641],
                    [-6.524237394332887, 53.37748110403081],
                    [-6.526050567626954, 53.377429875206566]
                ]
            ],
            "partOf": "urn:ngsi-ld:Building:0"
        },
        {
            "id": "urn:ngsi-ld:Building:2",
            "name": "FAB 2",
            "description": "Semiconductor manufacturing site",
            "category": "industrial",
            "peopleCapacity": 300,
            "peopleOccupancy": 130,
            "coordinates": [
                [
                    [-6.528700590133668, 53.37623951860026],
                    [-6.528818607330323, 53.37746902773945],
                    [-6.526254415512086, 53.377564699115155],
                    [-6.52614712715149, 53.37632233395982],
                    [-6.528700590133668, 53.37623951860026]
                ]
            ],
            "cleanrooms": ["urn:ngsi-ld:Building:3"]
        },
        {
            "id": "urn:ngsi-ld:Building:3",
            "name": "Cleanroom 2",
            "description": "Wafer fabrication cleanroom",
            "category": "industrial",
            "peopleCapacity": 160,
            "peopleOccupancy": 90,
            "coordinates": [
                [
                    [-6.526705026626588, 53.377474700431144],
                    [-6.528314352035523, 53.377404260771314],
                    [-6.5281856060028085, 53.37672547262395],
                    [-6.526619195938111, 53.376776702295544],
                    [-6.526705026626588, 53.377474700431144]
                ]
            ],
            "partOf": "urn:ngsi-ld:Building:2"
        },
        {
            "id": "urn:ngsi-ld:Building:4",
            "name": "FAB 10",
            "description": "Semiconductor manufacturing site",
            "category": "industrial",
            "peopleCapacity": 240,
            "peopleOccupancy": 200,
            "coordinates": [
                [
                    [-6.523529291152955, 53.375317196085284],
                    [-6.523110866546632, 53.375848718506596],
                    [-6.5229928493499765, 53.37581669927139],
                    [-6.522778272628785, 53.37606644866757],
                    [-6.521126031875611, 53.37559896783359],
                    [-6.521608829498292, 53.37499699865389],
                    [-6.521362066268922, 53.37489453496744],
                    [-6.521501541137696, 53.374734434963834],
                    [-6.523529291152955, 53.375317196085284]
                ]
            ],
            "cleanrooms": ["urn:ngsi-ld:Building:5"]
        },
        {
            "id": "urn:ngsi-ld:Building:5",
            "name": "Cleanroom 3",
            "description": "Wafer fabrication cleanroom",
            "category": "industrial",
            "peopleCapacity": 130,
            "peopleOccupancy": 70,
            "coordinates": [
                [
                    [-6.521608829498292, 53.37499699865389],
                    [-6.523443460464478, 53.37546460785836],
                    [-6.523110866546632, 53.375848718506596],
                    [-6.5229928493499765, 53.37581669927139],
                    [-6.521340608596803, 53.375354855022145],
                    [-6.521608829498292, 53.37499699865389]
                ]
            ],
            "partOf": "urn:ngsi-ld:Building:4"
        },
        {
            "id": "urn:ngsi-ld:Building:6",
            "name": "FAB 14",
            "description": "Semiconductor manufacturing site",
            "category": "industrial",
            "peopleCapacity": 250,
            "peopleOccupancy": 110,
            "coordinates": [
                [
                    [-6.521431803703309, 53.37481074045667],
                    [-6.521367430686952, 53.374900396372176],
                    [-6.521185040473939, 53.37486197243149],
                    [-6.521029472351075, 53.37506049575191],
                    [-6.520916819572449, 53.37502207195567],
                    [-6.520439386367798, 53.37559930597922],
                    [-6.51989221572876, 53.375477632044806],
                    [-6.519870758056641, 53.37552886321747],
                    [-6.519677639007569, 53.375477632044806],
                    [-6.519613265991212, 53.37552886321747],
                    [-6.5194952487945566, 53.375484035944766],
                    [-6.5194952487945566, 53.37542640081057],
                    [-6.518594026565553, 53.375170243714834],
                    [-6.5193235874176025, 53.374222449064646],
                    [-6.521431803703309, 53.37481074045667]
                ]
            ],
            "cleanrooms": ["urn:ngsi-ld:Building:7"]
        },
        {
            "id": "urn:ngsi-ld:Building:7",
            "name": "Cleanroom 4",
            "description": "Wafer fabrication cleanroom",
            "category": "industrial",
            "peopleCapacity": 130,
            "peopleOccupancy": 70,
            "coordinates": [
                [
                    [-6.519387960433961, 53.37465356377178],
                    [-6.52089536190033, 53.375021793579506],
                    [-6.520434021949769, 53.37560134882825],
                    [-6.519913673400879, 53.37546686709752],
                    [-6.519860029220582, 53.375530906069876],
                    [-6.51966691017151, 53.37547647294951],
                    [-6.519618630409242, 53.37552770412355],
                    [-6.519489884376527, 53.375492482698],
                    [-6.519516706466676, 53.375438049528555],
                    [-6.518588662147523, 53.375153074741085],
                    [-6.518990993499757, 53.37468558388144],
                    [-6.519280672073364, 53.37478484606841],
                    [-6.519387960433961, 53.37465356377178]
                ]
            ],
            "partOf": "urn:ngsi-ld:Building:6"
        },
        {
            "id": "urn:ngsi-ld:Building:8",
            "name": "FAB 10 ENERGY CENTRE",
            "description": "Energy and utilities building supporting FAB 10",
            "category": "industrial",
            "peopleCapacity": 50,
            "peopleOccupancy": 20,
            "coordinates": [
                [
                    [-6.521217226982118, 53.37592753909454],
                    [-6.520745158195496, 53.376443044513564],
                    [-6.520337462425233, 53.37633097864892],
                    [-6.520814895629884, 53.375812269948476],
                    [-6.521217226982118, 53.37592753909454]
                ]
            ]
        },
        {
            "id": "urn:ngsi-ld:Building:9",
            "name": "FAB 14 ENERGY CENTRE",
            "description": "Energy and utilities building supporting FAB 14",
            "category": "industrial",
            "peopleCapacity": 50,
            "peopleOccupancy": 20,
            "coordinates": [
                [
                    [-6.520058512687684, 53.37566577185418],
                    [-6.520573496818543, 53.375816262583626],
                    [-6.520010232925416, 53.3765046708426],
                    [-6.519511342048646, 53.376357384429866],
                    [-6.520058512687684, 53.37566577185418]
                ]
            ]
        },
        {
            "id": "urn:ngsi-ld:Building:10",
            "name": "R&D",
            "description": "Research and Development facility",
            "category": "industrial",
            "peopleCapacity": 100,
            "peopleOccupancy": 40,
            "coordinates": [
                [
                    [ -6.527069807052612, 53.37494908205687 ],
                    [ -6.526136398315431, 53.374673710030734 ],
                    [ -6.525986194610597, 53.37485942624383 ],
                    [ -6.525701880455018, 53.374804992265275 ],
                    [ -6.5252888202667245, 53.37532691519533 ],
                    [ -6.526120305061341, 53.37557346552081 ],
                    [ -6.526576280593873, 53.37560228299815 ],
                    [ -6.527069807052612, 53.37494908205687 ]
                ]
            ]
        },
        {
            "id": "urn:ngsi-ld:Building:11",
            "name": "IR5",
            "description": "Office building",
            "category": "office",
            "peopleCapacity": 200,
            "peopleOccupancy": 150,
            "coordinates": [
                [
                    [-6.525465846061707, 53.37509619572608],
                    [-6.524838209152223, 53.37595431742426],
                    [-6.524097919464112, 53.375746192481174],
                    [-6.524430513381958, 53.37528831402632],
                    [-6.524575352668763, 53.37528831402632],
                    [-6.524709463119508, 53.375102599683366],
                    [-6.524832844734193, 53.37512821550295],
                    [-6.525079607963563, 53.37506737790628],
                    [-6.52512788772583, 53.374984126317386],
                    [-6.525465846061707, 53.37509619572608]
                ]
            ]
        },
        {
            "id": "urn:ngsi-ld:Building:12",
            "name": "IR2",
            "description": "Office building",
            "category": "office",
            "peopleCapacity": 200,
            "peopleOccupancy": 150,
            "coordinates": [
                [
                    [-6.524580717086792, 53.37528850017854],
                    [-6.524430513381958, 53.375285298213996],
                    [-6.524049639701844, 53.375154017459934],
                    [-6.523738503456117, 53.37554785850806],
                    [-6.523443460464478, 53.37546460785836],
                    [-6.523534655570984, 53.37531091392368],
                    [-6.521490812301637, 53.37474096074059],
                    [-6.521726846694947, 53.37444317317883],
                    [-6.523700952529908, 53.37503234225342],
                    [-6.523759961128236, 53.37495549457545],
                    [-6.524028182029725, 53.37501953431671],
                    [-6.523974537849427, 53.37509638187914],
                    [-6.524580717086792, 53.37528850017854]
                ]
            ]
        },
        {
            "id": "urn:ngsi-ld:Building:13",
            "name": "RODI",
            "description": "Reverse Osmosis Deionized Water facility",
            "category": "industrial",
            "peopleCapacity": 50,
            "peopleOccupancy": 20,
            "coordinates": [
                [
                    [-6.520981192588806, 53.37639831383845],
                    [-6.521458625793458, 53.376529590756995],
                    [-6.521474719047547, 53.37649437016002],
                    [-6.522032618522645, 53.376644857961594],
                    [-6.52187705039978, 53.37684017112388],
                    [-6.520857810974122, 53.376574416929195],
                    [-6.520981192588806, 53.37639831383845]
                ]
            ]
        },
        {
            "id": "urn:ngsi-ld:Building:14",
            "name": "ASU",
            "description": "Air Separation Units",
            "category": "industrial",
            "peopleCapacity": 50,
            "peopleOccupancy": 20,
            "coordinates": [
                [
                    [-6.522515416145326, 53.376516783270574],
                    [-6.522070169448853, 53.37640471759997],
                    [-6.522161364555359, 53.376295853523295],
                    [-6.522590517997743, 53.37641112136052],
                    [-6.522515416145326, 53.376516783270574]
                ]
            ]
        },
        {
            "id": "urn:ngsi-ld:Building:15",
            "name": "Ryebrook 110kV Substation",
            "description": "High-voltage power substation",
            "category": "industrial",
            "peopleCapacity": 20,
            "peopleOccupancy": 10,
            "coordinates": [
                [
                    [-6.522858738899231, 53.377563374427105],
                    [-6.5229445695877075, 53.37766262990698],
                    [-6.522182822227478, 53.37791236847818],
                    [-6.522080898284913, 53.37780350825541],
                    [-6.522858738899231, 53.377563374427105]
                ]
            ]
        },
        {
            "id": "urn:ngsi-ld:Building:16",
            "name": "Waste Water Treatment Building",
            "description": "Waste water treatment facility",
            "category": "industrial",
            "peopleCapacity": 50,
            "peopleOccupancy": 20,
            "coordinates": [
                [
                    [-6.525503396987916, 53.378319608644944],
                    [-6.52614712715149, 53.378300398221334],
                    [-6.52614712715149, 53.37824276689846],
                    [-6.52861475944519, 53.37816592501335],
                    [-6.52863621711731, 53.37842206409124],
                    [-6.5270912647247314, 53.37847329172193],
                    [-6.5270912647247314, 53.37856293992739],
                    [-6.525567770004273, 53.378607763959366],
                    [-6.525503396987916, 53.378319608644944]
                ]
            ]
        },
        {
            "id": "urn:ngsi-ld:Building:17",
            "name": "Water Treatment Building",
            "description": "Water treatment facility",
            "category": "industrial",
            "peopleCapacity": 50,
            "peopleOccupancy": 20,
            "coordinates": [
                [
                    [-6.525492668151856, 53.378320223415884],
                    [-6.525492668151856, 53.37862118558356],
                    [-6.5230679512023935, 53.37868521981287],
                    [-6.523025035858155, 53.37837785463393],
                    [-6.525492668151856, 53.378320223415884]
                ]
            ]
        },
        {
            "id": "urn:ngsi-ld:Building:18",
            "name": "MSCP",
            "description": "Multi-Storey Car Park",
            "category": "parking",
            "peopleCapacity": 500,
            "peopleOccupancy": 10,
            "coordinates": [
                [
                    [ -6.52462363243103, 53.37461906745764 ],
                    [ -6.521978974342347, 53.37417071471709 ],
                    [ -6.5222471952438354, 53.37360074627563 ],
                    [ -6.52490258216858, 53.37405544081614 ],
                    [ -6.52462363243103, 53.37461906745764 ]
                ]
            ]
        }
    ]

# =================== Person Data ===================
from faker import Faker
fk = Faker()

person_data = [
        {
            "id": "urn:ngsi-ld:Person:0",
            "type": "Person",
            "name": fk.name(),
            "hasDevices": [],
            "currentFacility": "urn:ngsi-ld:Building:0",
            "role": "Engineer"
        },
        {
            "id": "urn:ngsi-ld:Person:1",
            "type": "Person",
            "name": fk.name(),
            "hasDevices": [],
            "currentFacility": "urn:ngsi-ld:Building:0",
            "role": "Janitor"
        },
        {
            "id": "urn:ngsi-ld:Person:2",
            "type": "Person",
            "name": fk.name(),
            "hasDevices": [],
            "currentFacility": "urn:ngsi-ld:Building:1",
            "role": "Technician"
        },
        {
            "id": "urn:ngsi-ld:Person:3",
            "type": "Person",
            "name": fk.name(),
            "hasDevices": [],
            "currentFacility": "urn:ngsi-ld:Building:1",
            "role": "Cleanroom Operator"
        },
        {
            "id": "urn:ngsi-ld:Person:4",
            "type": "Person",
            "name": fk.name(),
            "hasDevices": [],
            "currentFacility": "urn:ngsi-ld:Building:2",
            "role": "Technician"
        },
        {
            "id": "urn:ngsi-ld:Person:5",
            "type": "Person",
            "name": fk.name(),
            "hasDevices": [],
            "currentFacility": "urn:ngsi-ld:Building:2",
            "role": "Engineer"
        },
        {
            "id": "urn:ngsi-ld:Person:6",
            "type": "Person",
            "name": fk.name(),
            "hasDevices": [],
            "currentFacility": "urn:ngsi-ld:Building:3",
            "role": "Cleanroom Operator"
        },
        {
            "id": "urn:ngsi-ld:Person:7",
            "type": "Person",
            "name": fk.name(),
            "hasDevices": [],
            "currentFacility": "urn:ngsi-ld:Building:3",
            "role": "Cleanroom Operator"
        },
        {
            "id": "urn:ngsi-ld:Person:8",
            "type": "Person",
            "name": fk.name(),
            "hasDevices": [],
            "currentFacility": "urn:ngsi-ld:Building:4",
            "role": "Technician"
        },
        {
            "id": "urn:ngsi-ld:Person:9",
            "type": "Person",
            "name": fk.name(),
            "hasDevices": [],
            "currentFacility": "urn:ngsi-ld:Building:4",
            "role": "Engineer"

        },
        {
            "id": "urn:ngsi-ld:Person:10",
            "type": "Person",
            "name": fk.name(),
            "hasDevices": [],
            "currentFacility": "urn:ngsi-ld:Building:5",
            "role": "Cleanroom Operator"
        }
    ]

# =================== Device Data ===================

device_trackers_data = [
    {
        "id": "urn:ngsi-ld:Device:0",
        "type": "Device",
        "name": "BluetoothTracker-0",
        "description": "Bluetooth tracker for asset tracking",
        "deviceCategory": ["meter"],
        "controlledProperty": ["location"],
        "controlledAsset": ["urn:ngsi-ld:Person:0"],
        "supportedProtocol": ["bluetooth LE", "bluetooth"],
        "coordinates": [
            float(fk.longitude()),
            float(fk.latitude())
        ],
        "rssi": fk.random_int(min=-120, max=0),
        "batteryLevel": fk.random_int(min=0, max=100),
        "dateLastValueReported": fk.date_time_this_month().isoformat()
    },
    {
        "id": "urn:ngsi-ld:Device:1",
        "type": "Device",
        "name": "BluetoothTracker-1",
        "description": "Bluetooth tracker for asset tracking",
        "deviceCategory": ["meter"],
        "controlledProperty": ["location"],
        "controlledAsset": ["urn:ngsi-ld:Person:1"],
        "supportedProtocol": ["bluetooth LE", "bluetooth"],
        "coordinates": [
            float(fk.longitude()),
            float(fk.latitude())
        ],
        "rssi": fk.random_int(min=-120, max=0),
        "batteryLevel": fk.random_int(min=0, max=100),
        "dateLastValueReported": fk.date_time_this_month().isoformat()
    },
    {
        "id": "urn:ngsi-ld:Device:2",
        "type": "Device",
        "name": "BluetoothTracker-2",
        "description": "Bluetooth tracker for asset tracking",
        "deviceCategory": ["meter"],
        "controlledProperty": ["location"],
        "controlledAsset": ["urn:ngsi-ld:Person:2"],
        "supportedProtocol": ["bluetooth LE", "bluetooth"],
        "coordinates": [
            float(fk.longitude()),
            float(fk.latitude())
        ],
        "rssi": fk.random_int(min=-120, max=0),
        "batteryLevel": fk.random_int(min=0, max=100),
        "dateLastValueReported": fk.date_time_this_month().isoformat()
    },
    {
        "id": "urn:ngsi-ld:Device:3",
        "type": "Device",
        "name": "BluetoothTracker-3",
        "description": "Bluetooth tracker for asset tracking",
        "deviceCategory": ["meter"],
        "controlledProperty": ["location"],
        "controlledAsset": ["urn:ngsi-ld:Person:3"],
        "supportedProtocol": ["bluetooth LE", "bluetooth"],
        "coordinates": [
            float(fk.longitude()),
            float(fk.latitude())
        ],
        "rssi": fk.random_int(min=-120, max=0),
        "batteryLevel": fk.random_int(min=0, max=100),
        "dateLastValueReported": fk.date_time_this_month().isoformat()
    },
    {
        "id": "urn:ngsi-ld:Device:4",
        "type": "Device",
        "name": "BluetoothTracker-4",
        "description": "Bluetooth tracker for asset tracking",
        "deviceCategory": ["meter"],
        "controlledProperty": ["location"],
        "controlledAsset": ["urn:ngsi-ld:Person:4"],
        "supportedProtocol": ["bluetooth LE", "bluetooth"],
        "coordinates": [
            float(fk.longitude()),
            float(fk.latitude())
        ],
        "rssi": fk.random_int(min=-120, max=0),
        "batteryLevel": fk.random_int(min=0, max=100),
        "dateLastValueReported": fk.date_time_this_month().isoformat()
    },
    {
        "id": "urn:ngsi-ld:Device:5",
        "type": "Device",
        "name": "BluetoothTracker-5",
        "description": "Bluetooth tracker for asset tracking",
        "deviceCategory": ["meter"],
        "controlledProperty": ["location"],
        "controlledAsset": ["urn:ngsi-ld:Person:5"],
        "supportedProtocol": ["bluetooth LE", "bluetooth"],
        "coordinates": [
            float(fk.longitude()),
            float(fk.latitude())
        ],
        "rssi": fk.random_int(min=-120, max=0),
        "batteryLevel": fk.random_int(min=0, max=100),
        "dateLastValueReported": fk.date_time_this_month().isoformat()
    },
    {
        "id": "urn:ngsi-ld:Device:6",
        "type": "Device",
        "name": "BluetoothTracker-6",
        "description": "Bluetooth tracker for asset tracking",
        "deviceCategory": ["meter"],
        "controlledProperty": ["location"],
        "controlledAsset": ["urn:ngsi-ld:Person:6"],
        "supportedProtocol": ["bluetooth LE", "bluetooth"],
        "coordinates": [
            float(fk.longitude()),
            float(fk.latitude())
        ],
        "rssi": fk.random_int(min=-120, max=0),
        "batteryLevel": fk.random_int(min=0, max=100),
        "dateLastValueReported": fk.date_time_this_month().isoformat()
    },
    {
        "id": "urn:ngsi-ld:Device:7",
        "type": "Device",
        "name": "BluetoothTracker-7",
        "description": "Bluetooth tracker for asset tracking",
        "deviceCategory": ["meter"],
        "controlledProperty": ["location"],
        "controlledAsset": ["urn:ngsi-ld:Person:7"],
        "supportedProtocol": ["bluetooth LE", "bluetooth"],
        "coordinates": [
            float(fk.longitude()),
            float(fk.latitude())
        ],
        "rssi": fk.random_int(min=-120, max=0),
        "batteryLevel": fk.random_int(min=0, max=100),
        "dateLastValueReported": fk.date_time_this_month().isoformat()
    },
    {
        "id": "urn:ngsi-ld:Device:8",
        "type": "Device",
        "name": "BluetoothTracker-8",
        "description": "Bluetooth tracker for asset tracking",
        "deviceCategory": ["meter"],
        "controlledProperty": ["location"],
        "controlledAsset": ["urn:ngsi-ld:Person:8"],
        "supportedProtocol": ["bluetooth LE", "bluetooth"],
        "coordinates": [
            float(fk.longitude()),
            float(fk.latitude())
        ],
        "rssi": fk.random_int(min=-120, max=0),
        "batteryLevel": fk.random_int(min=0, max=100),
        "dateLastValueReported": fk.date_time_this_month().isoformat()
    },
    {
        "id": "urn:ngsi-ld:Device:9",
        "type": "Device",
        "name": "BluetoothTracker-9",
        "description": "Bluetooth tracker for asset tracking",
        "deviceCategory": ["meter"],
        "controlledProperty": ["location"],
        "controlledAsset": ["urn:ngsi-ld:Person:9"],
        "supportedProtocol": ["bluetooth LE", "bluetooth"],
        "coordinates": [
            float(fk.longitude()),
            float(fk.latitude())
        ],
        "rssi": fk.random_int(min=-120, max=0),
        "batteryLevel": fk.random_int(min=0, max=100),
        "dateLastValueReported": fk.date_time_this_month().isoformat()
    },
    {
        "id": "urn:ngsi-ld:Device:10",
        "type": "Device",
        "name": "BluetoothTracker-10",
        "description": "Bluetooth tracker for asset tracking",
        "deviceCategory": ["meter"],
        "controlledProperty": ["location"],
        "controlledAsset": ["urn:ngsi-ld:Person:10"],
        "supportedProtocol": ["bluetooth LE", "bluetooth"],
        "coordinates": [
            float(fk.longitude()),
            float(fk.latitude())
        ],
        "rssi": fk.random_int(min=-120, max=0),
        "batteryLevel": fk.random_int(min=0, max=100),
        "dateLastValueReported": fk.date_time_this_month().isoformat()
    },
    {
        "id": "urn:ngsi-ld:Device:11",
        "type": "Device",
        "name": "GPSTracker-0",
        "description": "GPS tracker for asset tracking outdoors",
        "deviceCategory": ["meter"],
        "controlledProperty": ["location"],
        "controlledAsset": ["urn:ngsi-ld:Person:0"],
        "supportedProtocol": ["lora"],
        "coordinates": [
            float(fk.longitude()),
            float(fk.latitude())
        ],
        "rssi": fk.random_int(min=-120, max=0),
        "batteryLevel": fk.random_int(min=0, max=100),
        "dateLastValueReported": fk.date_time_this_month().isoformat()
    },
    {
        "id": "urn:ngsi-ld:Device:12",
        "type": "Device",
        "name": "GPSTracker-1",
        "description": "GPS tracker for asset tracking outdoors",
        "deviceCategory": ["meter"],
        "controlledProperty": ["location"],
        "controlledAsset": ["urn:ngsi-ld:Person:1"],
        "supportedProtocol": ["lora"],
        "coordinates": [
            float(fk.longitude()),
            float(fk.latitude())
        ],
        "rssi": fk.random_int(min=-120, max=0),
        "batteryLevel": fk.random_int(min=0, max=100),
        "dateLastValueReported": fk.date_time_this_month().isoformat()
    },
    {
        "id": "urn:ngsi-ld:Device:13",
        "type": "Device",
        "name": "GPSTracker-2",
        "description": "GPS tracker for asset tracking outdoors",
        "deviceCategory": ["meter"],
        "controlledProperty": ["location"],
        "controlledAsset": ["urn:ngsi-ld:Person:2"],
        "supportedProtocol": ["lora"],
        "coordinates": [
            float(fk.longitude()),
            float(fk.latitude())
        ],
        "rssi": fk.random_int(min=-120, max=0),
        "batteryLevel": fk.random_int(min=0, max=100),
        "dateLastValueReported": fk.date_time_this_month().isoformat()
    },
    {
        "id": "urn:ngsi-ld:Device:14",
        "type": "Device",
        "name": "GPSTracker-3",
        "description": "GPS tracker for asset tracking outdoors",
        "deviceCategory": ["meter"],
        "controlledProperty": ["location"],
        "controlledAsset": ["urn:ngsi-ld:Person:3"],
        "supportedProtocol": ["lora"],
        "coordinates": [
            float(fk.longitude()),
            float(fk.latitude())
        ],
        "rssi": fk.random_int(min=-120, max=0),
        "batteryLevel": fk.random_int(min=0, max=100),
        "dateLastValueReported": fk.date_time_this_month().isoformat()
    },
    {
        "id": "urn:ngsi-ld:Device:15",
        "type": "Device",
        "name": "GPSTracker-4",
        "description": "GPS tracker for asset tracking outdoors",
        "deviceCategory": ["meter"],
        "controlledProperty": ["location"],
        "controlledAsset": ["urn:ngsi-ld:Person:4"],
        "supportedProtocol": ["lora"],
        "coordinates": [
            float(fk.longitude()),
            float(fk.latitude())
        ],
        "rssi": fk.random_int(min=-120, max=0),
        "batteryLevel": fk.random_int(min=0, max=100),
        "dateLastValueReported": fk.date_time_this_month().isoformat()
    },
    {
        "id": "urn:ngsi-ld:Device:16",
        "type": "Device",
        "name": "GPSTracker-5",
        "description": "GPS tracker for asset tracking outdoors",
        "deviceCategory": ["meter"],
        "controlledProperty": ["location"],
        "controlledAsset": ["urn:ngsi-ld:Person:5"],
        "supportedProtocol": ["lora"],
        "coordinates": [
            float(fk.longitude()),
            float(fk.latitude())
        ],
        "rssi": fk.random_int(min=-120, max=0),
        "batteryLevel": fk.random_int(min=0, max=100),
        "dateLastValueReported": fk.date_time_this_month().isoformat()
    },
    {
        "id": "urn:ngsi-ld:Device:17",
        "type": "Device",
        "name": "GPSTracker-6",
        "description": "GPS tracker for asset tracking outdoors",
        "deviceCategory": ["meter"],
        "controlledProperty": ["location"],
        "controlledAsset": ["urn:ngsi-ld:Person:6"],
        "supportedProtocol": ["lora"],
        "coordinates": [
            float(fk.longitude()),
            float(fk.latitude())
        ],
        "rssi": fk.random_int(min=-120, max=0),
        "batteryLevel": fk.random_int(min=0, max=100),
        "dateLastValueReported": fk.date_time_this_month().isoformat()
    },
    {
        "id": "urn:ngsi-ld:Device:18",
        "type": "Device",
        "name": "GPSTracker-7",
        "description": "GPS tracker for asset tracking outdoors",
        "deviceCategory": ["meter"],
        "controlledProperty": ["location"],
        "controlledAsset": ["urn:ngsi-ld:Person:7"],
        "supportedProtocol": ["lora"],
        "coordinates": [
            float(fk.longitude()),
            float(fk.latitude())
        ],
        "rssi": fk.random_int(min=-120, max=0),
        "batteryLevel": fk.random_int(min=0, max=100),
        "dateLastValueReported": fk.date_time_this_month().isoformat()
    },
    {
        "id": "urn:ngsi-ld:Device:19",
        "type": "Device",
        "name": "GPSTracker-8",
        "description": "GPS tracker for asset tracking outdoors",
        "deviceCategory": ["meter"],
        "controlledProperty": ["location"],
        "controlledAsset": ["urn:ngsi-ld:Person:8"],
        "supportedProtocol": ["lora"],
        "coordinates": [
            float(fk.longitude()),
            float(fk.latitude())
        ],
        "rssi": fk.random_int(min=-120, max=0),
        "batteryLevel": fk.random_int(min=0, max=100),
        "dateLastValueReported": fk.date_time_this_month().isoformat()
    },
    {
        "id": "urn:ngsi-ld:Device:20",
        "type": "Device",
        "name": "GPSTracker-9",
        "description": "GPS tracker for asset tracking outdoors",
        "deviceCategory": ["meter"],
        "controlledProperty": ["location"],
        "controlledAsset": ["urn:ngsi-ld:Person:9"],
        "supportedProtocol": ["lora"],
        "coordinates": [
            float(fk.longitude()),
            float(fk.latitude())
        ],
        "rssi": fk.random_int(min=-120, max=0),
        "batteryLevel": fk.random_int(min=0, max=100),
        "dateLastValueReported": fk.date_time_this_month().isoformat()
    },
    {
        "id": "urn:ngsi-ld:Device:21",
        "type": "Device",
        "name": "GPSTracker-10",
        "description": "GPS tracker for asset tracking outdoors",
        "deviceCategory": ["meter"],
        "controlledProperty": ["location"],
        "controlledAsset": ["urn:ngsi-ld:Person:10"],
        "supportedProtocol": ["lora"],
        "coordinates": [
            float(fk.longitude()),
            float(fk.latitude())
        ],
        "rssi": fk.random_int(min=-120, max=0),
        "batteryLevel": fk.random_int(min=0, max=100),
        "dateLastValueReported": fk.date_time_this_month().isoformat()
    }
]

door_data = [
    {
        "id": "urn:ngsi-ld:Door:0",
        "type": "Door",
        "areaServed": "Fab 1 Facility",
        "description": "Entrance to the Fab 1 facility",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.524827480316163, 53.37636733795882],
        "controlledBuildings": ["urn:ngsi-ld:Building:0"]
    },
    {
        "id": "urn:ngsi-ld:Door:1",
        "type": "Door",
        "areaServed": "Fab 1 Facility, Fab 10 Facility",
        "description": "Door connecting Fab 1 with Fab 10",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.522874832153321, 53.37601512933655],
        "controlledBuildings": ["urn:ngsi-ld:Building:0", "urn:ngsi-ld:Building:1"]
    },
    {
        "id": "urn:ngsi-ld:Door:2",
        "type": "Door",
        "areaServed": "Fab 2 Facility",
        "description": "Entrance to the Fab 2 facility",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.527380943298341, 53.37627768513132],
        "controlledBuildings": ["urn:ngsi-ld:Building:2"]
    },
    {
        "id": "urn:ngsi-ld:Door:3",
        "type": "Door",
        "areaServed": "Cleanroom 2",
        "description": "Entry into the Cleanroom 2",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.526683568954469, 53.37734710298634],
        "controlledBuildings": ["urn:ngsi-ld:Building:3"]
    },
    {
        "id": "urn:ngsi-ld:Door:4",
        "type": "Door",
        "areaServed": "Cleanroom 1",
        "description": "Entry into the Cleanroom 1",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.526007652282716, 53.376994902466876],
        "controlledBuildings": ["urn:ngsi-ld:Building:1"]
    },
    {
        "id": "urn:ngsi-ld:Door:5",
        "type": "Door",
        "areaServed": "IR2 Office Facility",
        "description": "Entry into the IR2 office building",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.523604393005372, 53.37501612176052],
        "controlledBuildings": ["urn:ngsi-ld:Building:12"]
    },
    {
        "id": "urn:ngsi-ld:Door:6",
        "type": "Door",
        "areaServed": "IR2 Office Facility, Fab 14 Facility",
        "description": "Door connecting IR2 with Fab 14",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.5216195583343515, 53.374574245550356],
        "controlledBuildings": ["urn:ngsi-ld:Building:12", "urn:ngsi-ld:Building:6"]
    }, #=======================================
    {
        "id": "urn:ngsi-ld:Door:7",
        "type": "Door",
        "areaServed": "IR2 Office Facility, Fab 10 Facility",
        "description": "Door connecting IR2 with Fab 10",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.521984338760376, 53.37488163818186],
        "controlledBuildings": ["urn:ngsi-ld:Building:12", "urn:ngsi-ld:Building:4"]
    },
    {
        "id": "urn:ngsi-ld:Door:8",
        "type": "Door",
        "areaServed": "Cleanroom 3",
        "description": "Entry into the Cleanroom 3",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.522338390350343, 53.375163614334994],
        "controlledBuildings": ["urn:ngsi-ld:Building:5"]
    },
    {
        "id": "urn:ngsi-ld:Door:9",
        "type": "Door",
        "areaServed": "Fab 14 Facility",
        "description": "Entrance to the Fab 14 facility",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.521083116531373, 53.37426705222773],
        "controlledBuildings": ["urn:ngsi-ld:Building:6"]
    },
    {
        "id": "urn:ngsi-ld:Door:10",
        "type": "Door",
        "areaServed": "Fab 14 Facility",
        "description": "Side entrance and exit to the Fab 14 facility",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.521093845367432, 53.3749458795584],
        "controlledBuildings": ["urn:ngsi-ld:Building:6"]
    },
    {
        "id": "urn:ngsi-ld:Door:11",
        "type": "Door",
        "areaServed": "Fab 14 Facility",
        "description": "Exit corridor from the Fab 14 facility",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.519141197204591, 53.374491194523905],
        "controlledBuildings": ["urn:ngsi-ld:Building:6"]
    },
    {
        "id": "urn:ngsi-ld:Door:12",
        "type": "Door",
        "areaServed": "Cleanroom 4",
        "description": "Entrance to the Cleanroom 4",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.519334316253663, 53.37472814366869],
        "controlledBuildings": ["urn:ngsi-ld:Building:7"]
    }, #=======================================
    {
        "id": "urn:ngsi-ld:Door:13",
        "type": "Door",
        "areaServed": "Cleanroom 4",
        "description": "Back exit from the Cleanroom 4",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.519763469696045, 53.37550302220792],
        "controlledBuildings": ["urn:ngsi-ld:Building:7"]
    },
    {
        "id": "urn:ngsi-ld:Door:14",
        "type": "Door",
        "areaServed": "IR5 Office Facility",
        "description": "Entrance into the IR5 office building",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.524634361267091, 53.37521484588535],
        "controlledBuildings": ["urn:ngsi-ld:Building:11"]
    },
    {
        "id": "urn:ngsi-ld:Door:15",
        "type": "Door",
        "areaServed": "R&D Lab",
        "description": "Front entrance to the R&D Lab",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.525557041168214, 53.37498430342339],
        "controlledBuildings": ["urn:ngsi-ld:Building:10"]
    },
    {
        "id": "urn:ngsi-ld:Door:16",
        "type": "Door",
        "areaServed": "R&D Lab",
        "description": "Back entrance to the R&D Lab",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.52590036392212, 53.375515829999216],
        "controlledBuildings": ["urn:ngsi-ld:Building:10"]
    },
    {
        "id": "urn:ngsi-ld:Door:17",
        "type": "Door",
        "areaServed": "R&D Lab",
        "description": "Innovation Lab entrance",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.526694297790528, 53.37475375971348],
        "controlledBuildings": ["urn:ngsi-ld:Building:10"]
    },
    {
        "id": "urn:ngsi-ld:Door:18",
        "type": "Door",
        "areaServed": "Fab 10 Energy Centre",
        "description": "Entrance and exit to the Fab 10 Energy Centre",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.5210187435150155, 53.37586163890846],
        "controlledBuildings": ["urn:ngsi-ld:Building:8"]
    }, #=======================================
    {
        "id": "urn:ngsi-ld:Door:19",
        "type": "Door",
        "areaServed": "Fab 14 Energy Centre",
        "description": "Entrance and exit to the Fab 14 Energy Centre",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.520332098007203, 53.37574636958403],
        "controlledBuildings": ["urn:ngsi-ld:Building:9"]
    },
    {
        "id": "urn:ngsi-ld:Door:20",
        "type": "Door",
        "areaServed": "RODI Plant",
        "description": "Entrance and exit to the RODI, or Reverse Osmosis Deionized, Plant",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.5218448638916025, 53.37659167071829],
        "controlledBuildings": ["urn:ngsi-ld:Building:13"]
    },
    {
        "id": "urn:ngsi-ld:Door:21",
        "type": "Door",
        "areaServed": "Ryebrook 110kV Substation",
        "description": "Entrance and exit to the Ryebrook 110kV Substation",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.5227675437927255, 53.377726867088725],
        "controlledBuildings": ["urn:ngsi-ld:Building:15"]
    },
    {
        "id": "urn:ngsi-ld:Door:22",
        "type": "Door",
        "areaServed": "Water Treatment Building",
        "description": "Entrance and exit to the Water Treatment Building",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.523625850677491, 53.37837838348491],
        "controlledBuildings": ["urn:ngsi-ld:Building:17"]
    },
    {
        "id": "urn:ngsi-ld:Door:23",
        "type": "Door",
        "areaServed": "Waste Water Treatment Building",
        "description": "Entrance and exit to the Waste Water Treatment Building",
        "openState": "closed",
        "openDuration": 0,
        "coordinates": [-6.528314352035523, 53.37816066514359],
        "controlledBuildings": ["urn:ngsi-ld:Building:16"]
    }
]
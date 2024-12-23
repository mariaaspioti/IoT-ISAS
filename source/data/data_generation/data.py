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
                    [-6.512, 53.364],
                    [-6.511, 53.364],
                    [-6.511, 53.365],
                    [-6.512, 53.365],
                    [-6.512, 53.364]
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
                    [-6.512, 53.364],
                    [-6.511, 53.364],
                    [-6.511, 53.365],
                    [-6.512, 53.365],
                    [-6.512, 53.364]
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
                    [-6.512, 53.364],
                    [-6.511, 53.364],
                    [-6.511, 53.365],
                    [-6.512, 53.365],
                    [-6.512, 53.364]
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
                    [-6.512, 53.364],
                    [-6.511, 53.364],
                    [-6.511, 53.365],
                    [-6.512, 53.365],
                    [-6.512, 53.364]
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
                    [-6.512, 53.364],
                    [-6.511, 53.364],
                    [-6.511, 53.365],
                    [-6.512, 53.365],
                    [-6.512, 53.364]
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
                    [-6.512, 53.364],
                    [-6.511, 53.364],
                    [-6.511, 53.365],
                    [-6.512, 53.365],
                    [-6.512, 53.364]
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
                    [-6.512, 53.364],
                    [-6.511, 53.364],
                    [-6.511, 53.365],
                    [-6.512, 53.365],
                    [-6.512, 53.364]
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
        "name": "Bluetooth Tracker",
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
        "name": "Bluetooth Tracker",
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
        "name": "Bluetooth Tracker",
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
        "name": "Bluetooth Tracker",
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
        "name": "Bluetooth Tracker",
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
        "name": "Bluetooth Tracker",
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
        "name": "Bluetooth Tracker",
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
        "name": "Bluetooth Tracker",
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
        "name": "Bluetooth Tracker",
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
        "name": "Bluetooth Tracker",
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
        "name": "Bluetooth Tracker",
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
        "name": "GPS Tracker",
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
        "name": "GPS Tracker",
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
        "name": "GPS Tracker",
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
        "name": "GPS Tracker",
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
        "name": "GPS Tracker",
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
        "name": "GPS Tracker",
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
        "name": "GPS Tracker",
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
        "name": "GPS Tracker",
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
        "name": "GPS Tracker",
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
        "name": "GPS Tracker",
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
        "name": "GPS Tracker",
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
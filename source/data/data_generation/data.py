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
                    [-6.512, 53.364],
                    [-6.511, 53.364],
                    [-6.511, 53.365],
                    [-6.512, 53.365],
                    [-6.512, 53.364]
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
                    [-6.512, 53.364],
                    [-6.511, 53.364],
                    [-6.511, 53.365],
                    [-6.512, 53.365],
                    [-6.512, 53.364]
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
                    [-6.512, 53.364],
                    [-6.511, 53.364],
                    [-6.511, 53.365],
                    [-6.512, 53.365],
                    [-6.512, 53.364]
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
                    [-6.512, 53.364],
                    [-6.511, 53.364],
                    [-6.511, 53.365],
                    [-6.512, 53.365],
                    [-6.512, 53.364]
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
                    [-6.512, 53.364],
                    [-6.511, 53.364],
                    [-6.511, 53.365],
                    [-6.512, 53.365],
                    [-6.512, 53.364]
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
                    [-6.512, 53.364],
                    [-6.511, 53.364],
                    [-6.511, 53.365],
                    [-6.512, 53.365],
                    [-6.512, 53.364]
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
                    [-6.512, 53.364],
                    [-6.511, 53.364],
                    [-6.511, 53.365],
                    [-6.512, 53.365],
                    [-6.512, 53.364]
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
                    [-6.512, 53.364],
                    [-6.511, 53.364],
                    [-6.511, 53.365],
                    [-6.512, 53.365],
                    [-6.512, 53.364]
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
                    [-6.512, 53.364],
                    [-6.511, 53.364],
                    [-6.511, 53.365],
                    [-6.512, 53.365],
                    [-6.512, 53.364]
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
                    [-6.512, 53.364],
                    [-6.511, 53.364],
                    [-6.511, 53.365],
                    [-6.512, 53.365],
                    [-6.512, 53.364]
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
                    [-6.512, 53.364],
                    [-6.511, 53.364],
                    [-6.511, 53.365],
                    [-6.512, 53.365],
                    [-6.512, 53.364]
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
                    [-6.512, 53.364],
                    [-6.511, 53.364],
                    [-6.511, 53.365],
                    [-6.512, 53.365],
                    [-6.512, 53.364]
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

device_data = [
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
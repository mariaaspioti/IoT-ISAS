# IoT-ISAS
---
IoT-ISAS (Industrial Spatial Authorization System) is a simulated smart security and access management system developed as an undergraduate project for an IoT course. Designed around a fictional scenario at Ireland's chip fabrication in Leixlip, the system models how personnel movement, role-based access control, and emergencies could be managed in an industrial setting. 

The project simulates the integration of a variety of devices, such as NFC tags and readers, Bluetooth and GPS trackers, smart locks, SOS buttons, and cameras. These devices communicate with the Orion Context Broker via IoT tools like MQTT, LoraWAN and HTTP. All data is then managed and visualized thourgh a centralized dashboard built with Node.js, React, SQlite, and InfluxDB.

Users can monitor worker locations, review historical movement data, respond to emergency alerts, schedule and track facility maintenance events, and manually control door access. While the system wasn't implemented in a real facility, some hardware components, namely an NFC reader and tags, a smart lock, an SOS button and a GPS tracker, were available and used during development and demostration.

## 🎥 Videos

### Personnel Tracking & Access Control 

__Personnel Tracking__ is simulated using predefined movement routes for each worker, enhanced with randomized noise to mimic real Bluetooth and GPS tracker data. Building polygons are used to determine whether a worker is indoors or outdoors, and the system selects either Bluetooth or GPS tracker data respectively. Movements are visualized live on the map, displaying each worker's current position along with a partial movement trail. 

__Access Control__ is role-based, meaning it is implemented based on each worker's assigned role, which determines the facilities they are authorized to enter. Each worker is assigned an NFC tag, which is scanned at NFC readers when entering or exiting a building or room.

While access control is not enforced in the general tracking simulation, we showcase a scenario using a real NFC reader, NFC tag, and smart lock. In the demo video, a technician (represented by the yellow marker near the bottom center of the map) scans their tag at the NFC reader which is linked to Fab 1 and is granted access, as shown by a blue marker appearing on the door in the map and the smart lock unlocking. The same technician then scans his tag at the NFC reader which is now linked to Cleanroom 1. Since their role doesn't authorize access to Cleanrooms, the smart lock remains locked, and a red marker appears on the door in the map to indicate the denied entry.

https://github.com/user-attachments/assets/2492adac-3ba0-4fd6-8320-3c37528405c1

### SOS Button - Alert in Dashboard

The SOS Button provided to all workers for emergencies, creates an alert that appears both as a mark on the map and in the Active Alerts list on the dashboard. Each alert diplays essential information, including who pressed the button, their coordinates and whether they are inside a building or outdoors. Security officers can handle the alert by unlocking all doors, activating the alarm, or dismissing the alert. 

The demo video shows a real SOS button press, the real time visual output in the dashboard and the alert being dismissed. 

https://github.com/user-attachments/assets/2be752e6-6724-42ab-83a6-3f0810d8ad1f

### Maintenance Scheduling

The SOS Button provided to all workers for emergencies, creates an alert that appears both as a mark on the map and in the Active Alerts list on the dashboard. Each alert diplays essential information, including who pressed the button, their coordinates and whether they are inside a building or outdoors. Security officers can handle the alert by unlocking all doors, activating the alarm, or dismissing the alert.

The demo video shows a real SOS button press, the real time visual output in the dashboard and the alert being dismissed. 

https://github.com/user-attachments/assets/939664b3-e0d0-475c-973e-9631ca7ab51b

### Worker Movement History View

Selecting _"Show historic routes"_ allows you to visualize the __movement paths__ of each worker for a chosen date and time span. Within that time span, a slider lets you further narrow the visible timeline to a custom range. 

This video showcases the trails of two simulated workers during 30-minute period

https://github.com/user-attachments/assets/3beb409a-ecd3-434e-b908-3d890954bd09



## Architecture
---
![System architecture](images/final-architecture.png)

## Start system
---
- Run gui_manage_system.py
- Press install
- Press start all

_Alternatively:_

- Go to IoT-devices folder
- Make sure to run all IoT Agents (camera, NFC, SmartLock, SOSButtons, Trackers)
- Run fakers beacon_mimic.py, button_mimic.py (to send SOS alerts), ( optional nfc_reader_mimic.py)
- Go to `./source.`
- Execute `npm install`
- Execute `npm run install-start:all`
- Visit http://localhost:3000


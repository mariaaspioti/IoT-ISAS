# IoT-ISAS
---
IoT-ISAS is a smart security and access management system designed to monitor personnel movement, manage authorized access, and handle emergency notifications. Using technologies like NFC Tags & Readers, Bluetooth & GPS trackers, smart locks, SOS buttons, and cameras, the system provides centralized control through a dashboard. It also supports scheduling and tracking facility maintenances, as well as viewing historical movement data for personnel.

## 🎥 Videos

### Personnel Tracking & Access Control 

https://github.com/user-attachments/assets/2492adac-3ba0-4fd6-8320-3c37528405c1

### SOS Button - Alert in Dashboard

https://github.com/user-attachments/assets/2be752e6-6724-42ab-83a6-3f0810d8ad1f

### Maintenance Scheduling
https://github.com/user-attachments/assets/939664b3-e0d0-475c-973e-9631ca7ab51b


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


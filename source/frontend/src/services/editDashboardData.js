import * as APICall from './api';

export const fetchTrackingData = async () => {
    try {
        // Fetch all devices' locations
        const data = await APICall.fetchAllDevicesLocations();
        // console.log('Device data:', data);


        // Fetch all devices' controlledAssets i.e. people being tracked
        const controlledAssets = await APICall.fetchAllDevicesControlledAssets();
        // console.log('Controlled assets data:', controlledAssets);
        // setPeople(controlledAssets);

        // const controlledAssetsMap = controlledAssets.reduce((acc, person) => ({
        //     ...acc,
        //     [person.device_id]: person
        //   }), {});
        // console.log("controlledAssetsMap:", controlledAssetsMap);


        // Determine the Facility in which the device is located
        const facilities = await APICall.findCurrentFacilities(data);
        // console.log('Facilities data:', facilities);

        // 1. Map each device to its facility
        const deviceFacilityMap = data.reduce((acc, device, index) => {
            acc[device.id] = facilities[index];
            return acc;
        }, {});

        // console.log("deviceFacilityMap:", JSON.stringify(deviceFacilityMap, null, 2));
        // console.log("deviceFacilityMap:", deviceFacilityMap);

        // 2. Map each person to their BT and GPS devices
        const personDevicesMap = data.reduce((acc, device) => {
            const personIds = device.controlledAsset || [];
            const isBT = device.name.startsWith('BluetoothTracker');
            personIds.forEach(personId => {
                if (!acc[personId]) acc[personId] = { bt: null, gps: null };
                isBT ? (acc[personId].bt = device) : (acc[personId].gps = device);
            });
            return acc;
        }, {});

        // console.log("personDevicesMap:", JSON.stringify(personDevicesMap, null, 2));
        // console.log("personDevicesMap:", personDevicesMap);

        // 3. Build mapData based on people and their indoor/outdoor status
        let mapData = controlledAssets.map(person => {
            // console.log("person:", person);
            const devices = personDevicesMap[person.person_id]|| {};
            // console.log("devices:", devices);
            const isIndoors = person.isIndoors;
            const selectedDevice = isIndoors ? devices.bt : devices.gps;
            // console.log("selectedDevice:", selectedDevice);
            
            if (!selectedDevice) {
                console.warn(`No device found for person ${person.person_id}`);
                // return { lat: 53.373289, lng: -6.521759, message: 'No device found' };
                return null;
            }

            const facility = deviceFacilityMap[selectedDevice.id];
            const lng = selectedDevice.lng;
            const lat = selectedDevice.lat;
            const initials = person.person_name.split(' ').map(n => n[0]).join('');
            // console.log("selectedDevice:", selectedDevice);
            const selectedDeviceNum = selectedDevice.id.split('Device:')[1];

            return {
                lat,
                lng,
                facility_name: facility?.name || 'Outside',
                facility_id: facility?.id || 'Outside',
                ...person,
                tracking_type: isIndoors ? 'Bluetooth' : 'GPS',
                message: `Device: ${selectedDeviceNum} | Facility: ${facility?.name || 'Outside'}, Person: ${initials}`
            };
        }).filter(Boolean);

        return { mapData, facilities, controlledAssets, data };
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }
};

export const showDoors = async () => {
    const data = await APICall.fetchDoorsLocations();
    // console.log('Door data:', data);
    // form: { id: 'Door1', location: { type: 'geo:json', value: {type: 'Point', coordinates: [ 51.5074, 0.1278 ] } } }

    const mapData = data.map((door, index) => {
        return {
            lat: door.location.value.coordinates[1],
            lng: door.location.value.coordinates[0],
            message: `Door: ${door.id}`
        };
    });

    return mapData;
}

export const showBuildings = async () => {
    const data = await APICall.fetchBuildingsLocations();
    // console.log('Building data in showBuildings:', data);
    // form: { id: 'Building1', location: { type: 'geo:json', value: {type: 'Polygon', coordinates: [ [ [ 51.5074, 0.1278 ], [ 51.5074, 0.1278 ], [ 51.5074, 0.1278 ] ] } } }

    const mapData = data.flatMap((building) => {
        const coordinates = building.location.value.coordinates[0];
        return coordinates.map(coord => ({
            lat: coord[1],
            lng: coord[0],
            name: building.name.value,
            message: `Building: ${building.id}`
        }));
    });

    return mapData;
}

export const fetchFormatAlertData = async (alertData, isNew = false) => {
    console.log("Alert Data:", alertData, "in fetchFormatAlertData");

    // Common functions
    const formatAlertDate = (dateString) => {
        return new Date(dateString).toLocaleString('en-US', {
            timeZone: 'UTC',
            year: 'numeric',
            month: 'numeric',
            day: 'numeric',
            hour: 'numeric',
            minute: 'numeric',
            second: 'numeric',
            hour12: true
        });
    };

    const getPersonAndDeviceData = async (alertData) => {
        const deviceName = alertData.alertSource.value[0];
        const [deviceData] = await APICall.fetchDeviceDataGivenName(deviceName);
        const personId = deviceData.controlledAsset.value;
        const personData = await APICall.fetchPersonData(personId);
        return { deviceData, personData };
    };

    const getFacilityData = async (coordinates) => {
        const locationData = { lat: coordinates[1], lng: coordinates[0] };
        const facilities = await APICall.findCurrentFacilities([locationData]);
        return facilities[0];
    };

    // Common data processing
    const { deviceData, personData } = await getPersonAndDeviceData(alertData);
    
    // Location handling
    let deviceLocation;
    if (isNew) {
        const deviceIds = personData.hasDevices.value;
        const devicesData = await Promise.all(deviceIds.map(deviceId => 
            APICall.fetchDeviceData(deviceId)
        ));
        
        deviceLocation = personData.isIndoors.value
            ? devicesData.find(d => d.name.value.startsWith('BluetoothTracker')).location.value.coordinates
            : devicesData.find(d => d.name.value.startsWith('GPS')).location.value.coordinates;

        await APICall.patchAlertLocation(alertData.id, {
            lat: deviceLocation[1],
            lng: deviceLocation[0]
        });
    } else {
        deviceLocation = alertData.location.value.coordinates;
    }

    const facility = await getFacilityData(deviceLocation);
    const formattedDate = formatAlertDate(alertData.dateIssued.value);

    // Common response structure
    const baseData = {
        id: alertData.id,
        description: alertData.description.value,
        severity: alertData.severity.value,
        status: alertData.status.value,
        frontend_timestamp: new Date().toLocaleString(),
        dateIssued: formattedDate,
        personName: personData.name.value,
        personId: personData.id,
        personCurrentLocation: deviceLocation,
        personCurrentFacility: facility.name ? facility.name : 'Outside'
    };

    console.log('Formatted alert data:', baseData);
    return baseData;
};

export const fetchAllFacilitiesData = async () => {
    const facilities = await APICall.fetchAllBuildingsData();
    const facilitiesData = facilities.map(facility => ({
        id: facility.id,
        name: facility.name.value,
        location: facility.location.value.coordinates[0],
        category: facility.category.value,
        description: facility.description.value,
        cleanrooms: facility?.cleanrooms?.value,
        peopleCapacity: facility.peopleCapacity.value,
    }));
    return facilitiesData;
}

export const fetchAllPeopleData = async () => {
    const people = await APICall.fetchAllPeopleData();
    const peopleData = people.map(person => ({
        id: person.id,
        name: person.name.value,
        isIndoors: person.isIndoors.value,
        currentFacility: person?.currentFacility?.value,    
        hasDevices: person.hasDevices.value,
        role: person.role.value,
    }));
    return peopleData;
}

export const postMaintenanceSchedule = async (scheduleData) => {
    const response = await APICall.postMaintenanceSchedule(scheduleData);
    return response;
}

export const fetchAuthorizationData = async (personId, buildingId) => {
    const response = await APICall.fetchAccessAuthorization(personId, buildingId);
    return response;
}

export const fetchScheduledMaintenanceData = async () => {
    const schedules = await APICall.fetchScheduledMaintenance();
    console.log("Schedules in fetchScheduledMaintenanceData:", schedules);
    const schedulesData = schedules.map(schedule => ({
        id: schedule.id,
        facilityId: schedule.facilityId,
        facilityName: schedule.facilityName,
        startTime: schedule.startTime,
        endTime: schedule.endTime,
        status: schedule.status,
        description: schedule.description,
        peopleIds: schedule.peopleIds,
        peopleNames: schedule.peopleNames,
    }));
    return schedulesData;
}

export const fetchActiveAlertsData = async () => {
    const alerts = await APICall.fetchActiveAlerts();
    // formattedAlerts = alerts.forEach(alert => {
    //     return fetchFormatAlertData(alert);
    // });
    const formattedAlerts = await Promise.all(alerts.map(alert => fetchFormatAlertData(alert, false)));
    console.log("Formatted Alerts in fetchActiveAlertsData:", formattedAlerts);
    return formattedAlerts;
}

export const patchUpdatedAlertStatusData = async (alertId, alertStatus) => {
    const response = await APICall.patchAlertStatus(alertId, alertStatus);
    return response;
}

export const patchUpdatedAlertActionData = async (alertId, alertAction) => {
    const response = await APICall.patchAlertAction(alertId, alertAction);
    return response;
}

export const fetchAllSmartLocksData = async () => {
    const smartlocks = await APICall.fetchAllSmartLocks();
    const smartlocksData = smartlocks.map(smartlock => ({
        id: smartlock.id,
        lat: smartlock.location.value.coordinates[1],
        lng: smartlock.location.value.coordinates[0],
        message: `SmartLock: ${smartlock.id}`,
        controlledAsset: smartlock.controlledAsset.value,
        deviceCategory: smartlock.deviceCategory.value,
        deviceState: smartlock.deviceState.value,
        entry: smartlock.entry.value,
        exit: smartlock.exit.value,
        hardLock: smartlock?.hardLock?.value,
        name: smartlock.name.value,
        serialNumber: smartlock.serialNumber.value,
        value: smartlock.value.value
    }));
    return smartlocksData;
}
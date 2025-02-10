import * as dbInterface from '../model/dbInterface.mjs';
import axios from 'axios';
import { unlockSmartLock } from './smartlockController.mjs';


const orionUrl = 'http://150.140.186.118:1026/v2/entities';
const fiwareService = 'ISAS';
const fiwareServicePath = '/test';
const getHeaders = {
    'Fiware-Service': fiwareService,
    'Fiware-ServicePath': fiwareServicePath,
};

let handleNFCDeviceUpdates = async (device, socket) => {

    try {
        const nfcReaderId = device.id;
        const nfcReaderUrl = `${orionUrl}/?type=Device&id=${nfcReaderId}`;

        const nfcReaderResponse = await axios.get(nfcReaderUrl, {
            headers: getHeaders,
            params: {
                attrs: 'controlledAsset'
            }
        });

        if (!nfcReaderResponse.data[0]?.controlledAsset) {
            console.error('Controlled asset not found for the specified NFC reader');
            return;
        }

        const smartLockId = nfcReaderResponse.data[0].controlledAsset.value[0];
        const smartLockUrl = `${orionUrl}/?type=Device&id=${smartLockId}`;
        const smartLockResponse = await axios.get(smartLockUrl, {
            headers: getHeaders
        });

        const smartLockData = smartLockResponse.data[0];

        const facility = getFacility(device.direction.value, smartLockData);
        
        
        if (!smartLockData.hardLock.value) {
            if (facility != '') {
                checkUidAuthorization(device.value.value, facility, (roleAccess) => {
                    if (roleAccess) {
                        // Handle authorized access
                        // socket.emit('accessGranted', { device, facility });
                        console.log("access granted")
                        unlockSmartLock(smartLockId);

                    } else {
                        // Handle unauthorized access
                        // socket.emit('accessDenied', { device, facility });
                        console.log("access denied");
                    }
                });
            } else {
                // The person is trying to go outside
                // We need to find the facility that they are in now
                const facilityPersonIsIn = getFacilityPersonIsIn(device.direction.value, smartLockData);
                checkUidAuthorization(device.value.value, facilityPersonIsIn, (roleAccess) => {
                    if (roleAccess) {
                        // If they originally had access to this area, unlock the door and let them go outside

                        // socket.emit('accessGranted', { device, facility });  
                        console.log("access granted")
                        unlockSmartLock(smartLockId);

                    } else {
                        // If they didn't have access to the area they are in now, log that they are inside 
                        // an unauthorized area
                        // socket.emit('accessDenied', { device, facility });
                        console.log("Inside unauthorized area");
                    }
                });
            }
        } else {
            console.log("Hardlock is active. Access is restricted until the security officer disables it.");
        }

    } catch (error) {
        console.error('Error handling NFC device updates:', error);
    }
};


let getPersonFromUid = async (uid) => {
    try {
        const nfcTagUrl = `${orionUrl}/?type=Device&q=serialNumber==${uid}`;
        const nfcTagResponse = await axios.get(nfcTagUrl, {
            headers: getHeaders
        });

        if (nfcTagResponse.data.length === 0) {
            console.error('NFC tag not found for the specified UID');
            return null;
        }

        const nfcTag = nfcTagResponse.data[0];
        const personId = nfcTag.controlledAsset.value[0];
        return personId;
    } catch (error) {
        console.error('Error fetching NFC tag:', error);
        return null;
    }
};


let checkUidAuthorization = async (uid, facilityCBId, callback) => {
    try {
        const personCBId = await getPersonFromUid(uid);
        if (!personCBId) {
            console.error('Person not found for the specified UID');
            return callback(false);
        }

        const facility = await dbInterface.getFacilityByCBId(facilityCBId);
        const facilityID = facility.facility_id;
        dbInterface.checkRoleAccessInFacility(personCBId, facilityID, (err, roleAccess) => {
            if (err) {
                console.error('Error checking role access in facility:', err);
                return callback(false);
            }
            callback(!!roleAccess);
        });
    } catch (error) {
        console.error('Error in checkUidAuthorization:', error);
        callback(false);
    }
};

let getFacility = (direction, smartlock) => {
    if (direction === 'Entry') {
        return smartlock.entry.value[0];
    } else if (direction === 'Exit') {
        return smartlock.exit.value[0];
    }
};


let getFacilityPersonIsIn = (direction, smartlock) => {
    if (direction === 'Entry') {
        return smartlock.exit.value[0];
    } else if (direction === 'Exit') {
        return smartlock.entry.value[0];
    }
};


export { handleNFCDeviceUpdates };

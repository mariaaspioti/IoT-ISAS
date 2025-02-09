import * as dbInterface from '../model/dbInterface.mjs';
import axios from 'axios';


const orionUrl = 'http://150.140.186.118:1026/v2/entities';
const fiwareService = 'ISAS';
const fiwareServicePath = '/test';
const getHeaders = {
    'Fiware-Service': fiwareService,
    'Fiware-ServicePath': fiwareServicePath,
};

let handleNFCDeviceUpdates = async (device, socket) => {
    console.log(device);

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
        // console.log('Smart Lock Data:', smartLockData);
        const facility  = getFacility(device.direction.value, smartLockData);
        console.log(facility);



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


let checkUidAuthorization = async (uid, facilityId) => {
    
    const personId = await getPersonFromUid(uid);
    if (!personId) {
        console.error('Person not found for the specified UID');
        return false;
    }
    else
    {
        console.log(personId);
    }
};

let getFacility = ( direction, smartlock) => {
    if (direction === 'Entry') {
        return smartlock.entry.value;
    } else if (direction === 'Exit') {
        return smartlock.exit.value;
    }
};

export { handleNFCDeviceUpdates };

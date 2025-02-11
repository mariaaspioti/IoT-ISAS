import axios from 'axios';

const orionUrl = 'http://150.140.186.118:1026/v2/entities';
const fiwareService = 'ISAS';
const fiwareServicePath = '/test';
const getHeaders = {
    'Fiware-Service': fiwareService,
    'Fiware-ServicePath': fiwareServicePath,
};

export const unlockSmartLock = async (smartLockId) => {
    try {
        const commandUrl = `${orionUrl}/${smartLockId}/attrs`;
        const commandPayload = {
                "deviceState": {
                    "type": "Text",
                    "value": "unlocked"
                },
                "value": {
                    "type": "Text",
                    "value": "1"
                },
                "dateLastValueReported": {
                    "type": "DateTime",
                    "value": new Date().toISOString()
                },
            };

        const response = await axios.patch(commandUrl, commandPayload, {
            headers: {
                'Content-Type': 'application/json',
                ...getHeaders
            }
        });

        if (response.status === 204) {
            console.log(`Smart lock ${smartLockId} unlocked successfully`);
        } else {
            console.error(`Failed to unlock smart lock ${smartLockId}:`, response.data);
        }
    } catch (error) {
        console.error('Error sending unlock command to smart lock:', error);
    }
};
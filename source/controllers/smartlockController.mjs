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


// export const lockSmartLock = async (smartLockId) => {
//     try {
//         const commandUrl = `${orionUrl}/${smartLockId}/attrs`;
//         const commandPayload = {
//                 "deviceState": {
//                     "type": "Text",
//                     "value": "locked"
//                 },
//                 "value": {
//                     "type": "Text",
//                     "value": "2"
//                 },
//                 "dateLastValueReported": {
//                     "type": "DateTime",
//                     "value": new Date().toISOString()
//                 },
//             };

//         const response = await axios.patch(commandUrl, commandPayload, {
//             headers: {
//                 'Content-Type': 'application/json',
//                 ...getHeaders
//             }
//         });

//         if (response.status === 204) {
//             console.log(`Smart lock ${smartLockId} locked successfully`);
//         } else {
//             console.error(`Failed to lock smart lock ${smartLockId}:`, response.data);
//         }
//     } catch (error) {
//         console.error('Error sending lock command to smart lock:', error);
//     }
// }


// export const disableSmartLock = async (smartLockId) => {
//     try {
//         const commandUrl = `${orionUrl}/${smartLockId}/attrs`;
//         const commandPayload = {
//                 "hardLock": {
//                     "type": "Boolean",
//                     "value": true
//                 },
//                 "dateLastValueReported": {
//                     "type": "DateTime",
//                     "value": new Date().toISOString()
//                 },
//             };

//         const response = await axios.patch(commandUrl, commandPayload, {
//             headers: {
//                 'Content-Type': 'application/json',
//                 ...getHeaders
//             }
//         });

//         if (response.status === 204) {
//             console.log(`Smart lock ${smartLockId} disabled successfully`);
//         } else {
//             console.error(`Failed to disable smart lock ${smartLockId}:`, response.data);
//         }
//     } catch (error) {
//         console.error('Error sending disable command to smart lock:', error);
//     }
// }

// export const enableSmartLock = async (smartLockId) => {
//     try {
//         const commandUrl = `${orionUrl}/${smartLockId}/attrs`;
//         const commandPayload = {
//                 "hardLock": {
//                     "type": "Boolean",
//                     "value": false
//                 },
//                 "dateLastValueReported": {
//                     "type": "DateTime",
//                     "value": new Date().toISOString()
//                 },
//             };

//         const response = await axios.patch(commandUrl, commandPayload, {
//             headers: {
//                 'Content-Type': 'application/json',
//                 ...getHeaders
//             }
//         });

//         if (response.status === 204) {
//             console.log(`Smart lock ${smartLockId} enabled successfully`);
//         } else {
//             console.error(`Failed to enable smart lock ${smartLockId}:`, response.data);
//         }
//     } catch (error) {
//         console.error('Error sending enable command to smart lock:', error);
//     }
// }


// export const handleEnableSmartLock = async (req, res) => {
//     const { id } = req.params;
//     try {
//         await enableSmartLock(id);
//         res.status(200).send(`Smart lock ${id} enabled successfully.`);
//     } catch (error) {
//         console.error('Error enabling smart lock:', error);
//         res.status(500).send('Internal server error.');
//     }
// };

// export const handleDisableSmartLock = async (req, res) => {
//     const { id } = req.params;
//     try {
//         await disableSmartLock(id);
//         res.status(200).send(`Smart lock ${id} disabled successfully.`);
//     } catch (error) {
//         console.error('Error disabling smart lock:', error);
//         res.status(500).send('Internal server error.');
//     }
// };


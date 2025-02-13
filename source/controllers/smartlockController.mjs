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


export const lockSmartLock = async (smartLockId) => {
    try {
        const commandUrl = `${orionUrl}/${smartLockId}/attrs`;
        const commandPayload = {
                "deviceState": {
                    "type": "Text",
                    "value": "locked"
                },
                "value": {
                    "type": "Text",
                    "value": "2"
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
            console.log(`Smart lock ${smartLockId} locked successfully`);
        } else {
            console.error(`Failed to lock smart lock ${smartLockId}:`, response.data);
        }
    } catch (error) {
        console.error('Error sending lock command to smart lock:', error);
    }
}


export const disableSmartLock = async (smartLockId) => {
    try {
        const commandUrl = `${orionUrl}/${smartLockId}/attrs`;
        const commandPayload = {
                "hardLock": {
                    "type": "Boolean",
                    "value": true
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
            console.log(`Smart lock ${smartLockId} disabled successfully`);
        } else {
            console.error(`Failed to disable smart lock ${smartLockId}:`, response.data);
        }
    } catch (error) {
        console.error('Error sending disable command to smart lock:', error);
    }
}

export const enableSmartLock = async (smartLockId) => {
    try {
        const commandUrl = `${orionUrl}/${smartLockId}/attrs`;
        const commandPayload = {
                "hardLock": {
                    "type": "Boolean",
                    "value": false
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
            console.log(`Smart lock ${smartLockId} enabled successfully`);
        } else {
            console.error(`Failed to enable smart lock ${smartLockId}:`, response.data);
        }
    } catch (error) {
        console.error('Error sending enable command to smart lock:', error);
    }
}


export const lockAndDisableUnlocking = async (smartLockId) => {
    try {
        commandUrl = `${orionUrl}/${smartLockId}/attrs`;
        commandPayload = {
                "deviceState": {
                    "type": "Text",
                    "value": "locked"
                },
                "hardLock": {
                    "type": "Boolean",
                    "value": true
                },
                "value": {
                    "type": "Text",
                    "value": "2"
                },
                "dateLastValueReported": {
                    "type": "DateTime",
                    "value": new Date().toISOString()
                },
            };


        console.log(`Smart lock ${smartLockId} locked and unlocking disabled successfully`);
    } catch (error) {
        console.error('Error sending lock and disable command to smart lock:', error);
    }
}

export const handleSmartLockAction = async (req, res) => {
    const id = req.params.id;
    const action = req.body.action;
  
    try {
      switch (action) {
        case 'unlock':
          await unlockSmartLock(id);
          res.status(200).json({ message: `Smart lock ${id} unlocked successfully.` });
          break;
        case 'lock':
          await lockSmartLock(id);
          res.status(200).json({ message: `Smart lock ${id} locked successfully.` });
          break;
        case 'disableUnlocking':
          await disableSmartLock(id);
          res.status(200).json({ message: `Smart lock ${id} unlocking disabled successfully.` });
          break;
        case 'enableUnlocking':
          await enableSmartLock(id);
          res.status(200).json({ message: `Smart lock ${id} unlocking enabled successfully.` });
          break;
        default:
          res.status(400).json({ error: 'Invalid action.' });
      }
    } catch (error) {
      console.error('Error handling smart lock action:', error);
      res.status(500).json({ error: 'Internal server error.' });
    }
  };

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


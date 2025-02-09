import express from 'express';
const router = express.Router();

import * as apiController from '../controllers/apiController.mjs';
import * as stateController from '../controllers/stateController.mjs';

router.get('/data', apiController.getData);
router.get('/all-data', apiController.getAllData);
router.post('/save-coordinates', apiController.saveCoordinates);

router.get('/devices/controlledAssets', apiController.getAllDevicesControlledAssets);
router.get('/devices/location', apiController.getAllDevicesLocationData);
router.get('/devices/:id/location', apiController.getDeviceLocationData);
router.get('/devices/:id', apiController.getDeviceData);
router.get('/devices/name/:name', apiController.getDeviceDataFromName);

router.get('/facilities', apiController.getAllFacilities);
router.get('/facilities/name-location', apiController.getFacilitiesNameAndLocation);
router.get('/facilities/:id/location', apiController.getFacilityLocationData);
router.post('/facilities/find', apiController.findCurrentFacilities);


router.get('/doors/location', apiController.getDoorsLocations);

router.get('/people/:id', apiController.getPersonData);
router.get('/people', apiController.getAllPeopleData);

router.get('/maintenances/scheduled', apiController.getScheduledMaintenances);
router.post('/maintenance', apiController.handleMaintenanceSchedule);

// router.post('/alert/sos', apiController.handleSOSAlert); // For Orion subscription
// router.get('/alert/sos', apiController.handleSOSAlert); // For polling
router.get('/alerts/active', apiController.getActiveAlerts);
router.patch('/alerts/:id/status', apiController.patchAlertStatus);

router.get('access-check', apiController.checkAccessAuthorization);

export {router as apiRoutes};
import express from 'express';
const router = express.Router();

import * as apiController from '../controllers/apiController.mjs';
import * as stateController from '../controllers/stateController.mjs';

router.get('/data', apiController.getData);
router.get('/all-data', apiController.getAllData);
router.post('/save-coordinates', apiController.saveCoordinates);

router.get('/devices/location', apiController.getAllDevicesLocationData);
router.get('/devices/:id/location', apiController.getDeviceLocationData);
router.get('/devices/controlledAssets', apiController.getAllDevicesControlledAssets);

router.get('/facilities', apiController.getFacilities);
router.post('/facilities/find', apiController.findCurrentFacilities);

router.get('/doors/location', apiController.getDoorsLocations);


export {router as apiRoutes};
import express from 'express';
const router = express.Router();

import * as apiController from '../controllers/apiController.mjs';

router.get('/data', apiController.getData);
router.get('/all-data', apiController.getAllData);
router.post('/save-coordinates', apiController.saveCoordinates);

export {router as apiRoutes};
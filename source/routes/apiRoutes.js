import express from 'express';
const router = express.Router();

import * as apiController from '../controllers/apiController.mjs';

router.get('/data', apiController.getData);
router.post('/save-coordinates', apiController.saveCoordinates);

export {router as apiRoutes};
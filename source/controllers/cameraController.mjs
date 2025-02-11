import fs from 'fs';
import path from 'path';

const folderPath = path.join(__dirname, '../frontend/public/cameraImages');
const imagePath = path.join(folderPath, 'latest_image.jpg');

export const getLatestImage = (req, res) => {
  fs.access(imagePath, fs.constants.F_OK, (err) => {
    if (err) {
      return res.status(404).send('Image not found');
    }

    res.sendFile(imagePath);
  });
};
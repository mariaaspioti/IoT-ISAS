import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const folderPath = path.join(__dirname, '../frontend/public/cameraImages');

export const getLatestImage = (req, res) => {
  fs.readdir(folderPath, (err, files) => {
    if (err) {
      console.error('Unable to scan directory:', err);
      return res.status(500).send('Unable to scan directory');
    }

    const images = files.filter(file => file.endsWith('.jpg')).sort().reverse();

    if (images.length === 0) {
      return res.status(404).send('No images found');
    }

    const latestImage = images[0];
    const imagePath = path.join(folderPath, latestImage);

    res.sendFile(imagePath);
  });
};
import axios from 'axios';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Fix __dirname for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Ensure the directory exists
const folderPath = path.join(__dirname, 'cameraImages');
if (!fs.existsSync(folderPath)) {
    fs.mkdirSync(folderPath, { recursive: true });
}

const url = 'http://150.140.186.118:1111/'; // Your stream URL

axios({
  method: 'get',
  url,
  responseType: 'stream', // Treat response as a stream
}).then((response) => {
  let buffer = '';

  response.data.on('data', (chunk) => {
    buffer += chunk.toString('binary'); // Append chunk data as binary

    // Detect boundaries between images
    const boundary = '--frame';
    const parts = buffer.split(boundary);
    buffer = parts.pop(); // Keep any leftover data

    parts.forEach((part) => {
      if (part.includes('Content-Type: image/jpeg')) {
        const imageData = part.split('\r\n\r\n')[1]; // Extract binary image data

        if (imageData) {
          const imageBuffer = Buffer.from(imageData, 'binary');

          // Generate a unique filename
          const filename = `image_${Date.now()}.jpg`;
          const filePath = path.join(folderPath, filename);

          // Save image
          fs.writeFileSync(filePath, imageBuffer);
          console.log(`Saved: ${filePath}`);
        }
      }
    });
  });

  response.data.on('end', () => {
    console.log('Stream ended.');
  });

}).catch((error) => {
  console.error('Error fetching the stream:', error);
});

import React, { useState, useEffect } from 'react';
import { fetchCameraImage } from '../../services/api.js';
import './CameraFeed.css';

const CameraFeed = () => {
  const [imageSrc, setImageSrc] = useState('');

  useEffect(() => {
    const fetchImage = async () => {
      try {
        const imageUrl = await fetchCameraImage();
        console.log('Fetched image URL:', imageUrl); // Debugging statement
        const newImageSrc = `${imageUrl}?t=${new Date().getTime()}`;
        setImageSrc(newImageSrc);
        console.log('Set image source:', newImageSrc); // Debugging statement
      } catch (error) {
        console.error('Error fetching camera image:', error);
      }
    };

    fetchImage();
    const interval = setInterval(fetchImage, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      {imageSrc ? <img src={imageSrc} alt="Camera Feed" /> : <p>Loading...</p>}
    </div>
  );
};

export default CameraFeed;
import requests
import os
import time
from dotenv import load_dotenv

# Load environment variables from the .env file in the parent 'source' directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

# Ensure the directory exists
folder_path = os.path.join(os.path.dirname(__file__), '../frontend/public/cameraImages')

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Get the camera stream URL from the environment variables
url = os.getenv('CAMERA_STREAM_URL')

if not url:
    raise ValueError("CAMERA_STREAM_URL not found in environment variables")

response = requests.get(url, stream=True)

if response.status_code == 200:
    buffer = b''

    for chunk in response.iter_content(chunk_size=1024):
        buffer += chunk

        # Detect boundaries between images
        boundary = b'--frame'
        parts = buffer.split(boundary)
        buffer = parts.pop()  # Keep any leftover data

        for part in parts:
            if b'Content-Type: image/jpeg' in part:
                image_data = part.split(b'\r\n\r\n')[1]  # Extract binary image data

                if image_data:
                    # Generate a unique filename
                    filename = f'image_{int(time.time() * 1000)}.jpg'
                    file_path = os.path.join(folder_path, filename)

                    # Save image
                    with open(file_path, 'wb') as f:
                        f.write(image_data)
                    print(f'Saved: {file_path}')

    print('Stream ended.')
else:
    print('Error fetching the stream:', response.status_code)
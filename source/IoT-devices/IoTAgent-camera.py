import requests
import os
import time
from dotenv import load_dotenv


# Function that saves the image with a unique name
def save_image(image_data, folder_path):
    # Name is based on timestamp
    timestamp = time.strftime('%Y%m%d%H%M%S')
    filename = f'image_{timestamp}.jpg'
    file_path = os.path.join(folder_path, filename)

    with open(file_path, 'wb') as f:
        f.write(image_data)
    print(f'Saved: {file_path}')

# Make sure that at most 5 images are saved in the public/camerafeed directory
    manage_saved_images(folder_path)

def manage_saved_images(folder_path):
    
    images = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
    images.sort(reverse=True) 

    for image in images[5:]:
        os.remove(os.path.join(folder_path, image))
        print(f'Deleted: {image}')

def save_camera_images():
    # Load environment variables from the .env file in the parent 'source' directory
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path)

    # Ensure the directory exists
    folder_path = os.path.join(os.path.dirname(__file__), '../frontend/public/cameraImages')

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Get the camera stream url from .env
    url = os.getenv('CAMERA_STREAM_URL')

    if not url:
        raise ValueError("CAMERA_STREAM_URL not found in environment variables")

    response = requests.get(url, stream=True)

    if response.status_code == 200:
        buffer = b''
        last_save_time = time.time()

        # read the response content in managable chuncks
        for chunk in response.iter_content(chunk_size=1024):
            buffer += chunk

            # Find where each image ends
            boundary = b'--frame'
            parts = buffer.split(boundary)
            buffer = parts.pop()  # The last part is not complete

            for part in parts:
                if b'Content-Type: image/jpeg' in part:
                    image_data = part.split(b'\r\n\r\n')[1]  # Extract binary image data

                    if image_data:
                        current_time = time.time()
                        if current_time - last_save_time >= 5:
                            save_image(image_data, folder_path)
                            last_save_time = current_time

        print('Stream ended.')
    else:
        print('Error fetching the stream:', response.status_code)

if __name__ == "__main__":
    save_camera_images()
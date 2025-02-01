import os
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file in the sibling 'source' directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'source', '.env')
load_dotenv(dotenv_path)


def unlock_smartlock():
    # Get the token from the environment variables
    token = os.getenv('AUTH_TOKEN')

    if not token:
        raise ValueError("No token found in the environment variables")

    # Define the URL and headers for the HTTP request
    url = 'https://api.nuki.io/smartlock/18043712356/action/unlock'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    payload = {}

    # Send the HTTP request
    response = requests.post(url, headers=headers, json=payload)

    # Check the response status code
    if response.status_code == 200:
        print('Unlock request was successful')
        print('Response:', response.json())
    else:
        print('Unlock request failed')
        print('Status code:', response.status_code)
        print('Response:', response.text)


def lock_smartlock():
    # Get the token from the environment variables
    token = os.getenv('AUTH_TOKEN')

    if not token:
        raise ValueError("No token found in the environment variables")

    # Define the URL and headers for the HTTP request
    url = 'https://api.nuki.io/smartlock/18043712356/action/lock'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    payload = {}

    # Send the HTTP request
    response = requests.post(url, headers=headers, json=payload)

    # Check the response status code
    if response.status_code == 200:
        print('Lock request was successful')
        print('Response:', response.json())
    else:
        print('Lock request failed')
        print('Status code:', response.status_code)
        print('Response:', response.text)


def main():
    action = input("Enter 'lock' to lock or 'unlock' to unlock the smartlock: ").strip().lower()
    if action == 'lock':
        lock_smartlock()
    elif action == 'unlock':
        unlock_smartlock()
    else:
        print("Invalid action. Please enter 'lock' or 'unlock'.")


if __name__ == "__main__":
    main()

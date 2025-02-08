import os
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file in the sibling 'source' directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'source', '.env')
load_dotenv(dotenv_path)


def unlock_smartlock():
    token = os.getenv('AUTH_TOKEN')
    if not token:
        raise ValueError("No token found in the environment variables")

    url = 'https://api.nuki.io/smartlock/18043712356/action/unlock'
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json',  # Add 'accept' header for consistency
    }

    # No payload sent
    response = requests.post(url, headers=headers)

    if response.status_code == 204:
        print('Unlock request was successful')
    else:
        print('Unlock request failed')
        print('Status code:', response.status_code)
        print('Response:', response.text)


def lock_smartlock():
    token = os.getenv('AUTH_TOKEN')
    if not token:
        raise ValueError("No token found in the environment variables")

    url = 'https://api.nuki.io/smartlock/18043712356/action/lock'
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json',  # Add 'accept' header for consistency
    }

    # No payload sent
    response = requests.post(url, headers=headers)

    if response.status_code == 204:
        print('Lock request was successful')
    else:
        print('Lock request failed')
        print('Status code:', response.status_code)
        print('Response:', response.text)
        
def get_smartlock_():
    token = os.getenv('AUTH_TOKEN')

    if not token:
        raise ValueError("No token found in the environment variables")
    
    url = 'https://api.nuki.io/smartlock'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}',
       
    }

    response = requests.get(url, headers=headers)

    # Print the response status code and JSON content
    print(response.status_code)
    print(response.json())


def main():
    
    # get_smartlock_()
    action = input("Enter 'lock' to lock or 'unlock' to unlock the smartlock: ").strip().lower()
    if action == 'lock':
        lock_smartlock()
    elif action == 'unlock':
        unlock_smartlock()
    else:
        print("Invalid action. Please enter 'lock' or 'unlock'.")



if __name__ == "__main__":
    main()

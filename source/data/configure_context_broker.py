import json
import requests

# Orion Context Broker URL
orion_url = "http://150.140.186.118:1026/v2"
fiware_service = "ISAS"
fiware_service_path = "/test"
# POST headers with Fiware-Service and Fiware-ServicePath
post_headers = {
    "Content-Type": "application/json",
    "Fiware-Service": fiware_service,
    "Fiware-ServicePath": fiware_service_path
}
# GET/DELETE headers with Fiware-Service and Fiware-ServicePath
gd_headers = {
    "Fiware-Service": fiware_service,
    "Fiware-ServicePath": fiware_service_path
}

LOCAL_ADDRESS = "localhost:3001"

def create_subscription(payload):
    '''Create a subscription in the Context Broker with the given payload'''
    
    response = requests.post(orion_url + "/subscriptions", headers=post_headers, json=payload)
    if response.status_code == 201:
        print("Subscription created successfully")
    else:
        print(f"Failed to create subscription with status code {response.status_code}, response: {response.text}")

def get_alert_subscription_payload():
    '''Return the payload for creating an alert subscription'''
    
    payload = {
        "description": "Alert subscription",
        "subject": {
            "entities": [
                {
                    "idPattern": ".*",
                    "type": "Alert"
                }
            ],
            "condition": {
                "attrs": [
                    "category",
                    "subCategory"
                ],
                "expression": {
                    "q": "category==security;subCategory==suspiciousAction",
                }
            }
        },
        "notification": {
            "http": {
                "url": f"http://{LOCAL_ADDRESS}/api/alert/sos"
            },
            "attrs": [
                "id",
                "alertSource",
                "category",
                "dateIssued",
                "severity",
                "name",
                "description",
                "status"
            ],
            "metadata": ["dateCreated", "dateModified"]
        },
        "throttling": 5 # The minimum time between notifications in seconds
    }
    return payload

def delete_subscriptions():
    '''Delete all subscriptions in the Context Broker'''
    print("Deleting all subscriptions")
    response = requests.get(orion_url + "/subscriptions", headers=gd_headers)

    if response.status_code == 200:
        subscriptions = response.json()
        print("Listing all subscriptions...")
        for subscription in subscriptions:
            print(json.dumps(subscription))

        for subscription in subscriptions:
            print(f"Deleting subscription: {subscription['id']}")
            userin = input("Press Enter to continue or q to exit:")
            if userin == "q":
                return
            response = requests.delete(orion_url + f"/subscriptions/{subscription['id']}", headers=gd_headers)
            if response.status_code == 204:
                print(f"Subscription {subscription['id']} deleted successfully")
            else:
                print(f"Failed to delete subscription {subscription['id']} with status code {response.status_code}, response: {response.text}")
    else:
        print(f"Failed to retrieve subscriptions with status code {response.status_code}, response: {response.text}")

def validate_alert_subscription():
    '''Validate the alert subscription by sending a test alert'''
    print("Sending test alert to validate subscription")
    data = {
        "id": "test-alert",
        "type": "Alert",
        "category": "security",
        "subCategory": "suspiciousAction",
        "severity": "high",
        "name": "Test Alert",
        "description": "This is a test alert",
        "status": "active",
        "dateIssued": "2021-06-01T12:00:00Z",
        "alertSource": "test-source"
    }

    entity = {
        "id": data["id"],
        "type": "Alert",
        "alertSource": {
            "type": "Relationship",
            "value": [
                "test-source"
            ]
        },
        "category": {
            "type": "Text",
            "value": "security"
        },
        "dateIssued": {
            "type": "DateTime",
            "value": data["dateIssued"]
        },
        "subCategory": {
            "type": "Text",
            "value": data["subCategory"]
        },
        "severity": {
            "type": "Text",
            "value": data["severity"]
        },
        "name": {
            "type": "Text",
            "value": data["name"]
        },
        "description": {
            "type": "Text",
            "value": data["description"]
        },
        "status": {
            "type": "Text",
            "value": data["status"]
        }
    }
    response = requests.post(orion_url + "/entities", headers=post_headers, json=entity)
    if response.status_code == 201:
        print("Test alert sent successfully")
    else:
        print(f"Failed to send test alert with status code {response.status_code}, response: {response.text}")

    # delete the test alert
    response = requests.delete(orion_url + f"/entities/{data['id']}", headers=gd_headers)
    if response.status_code == 204:
        print("Test alert deleted successfully")
    else:
        print(f"Failed to delete test alert with status code {response.status_code}, response: {response.text}")

    

def main():
    alert_sub_payload = get_alert_subscription_payload()
    create_subscription(alert_sub_payload)

    delete_subscriptions()
    # validate_alert_subscription()

if __name__ == "__main__":
    main()
import requests
from uuid import uuid4
import json

url = "http://127.0.0.1:8000/"
query = input("What do you want to send to the Agent:")
payload = {
    "jsonrpc": "2.0",
    "id": 202,
    "method": "tasks/send",
    "params": {
        "id": "144",
        "sessionId": str(uuid4()),
        "acceptedOutputModes": [
            "text"
        ],
        "message": {
            "role": "user",
            "parts": [
                {
                    "type": "text",
                    "text": query
                }
            ]
        }
    }
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, json=payload)

print("Status Code:", response.status_code)
try:
    print("Response JSON:", response.json())
except json.JSONDecodeError:
    print("Response Text:", response.text)

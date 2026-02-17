import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Claude API endpoint from environment
endpoint_url = os.getenv("ENDPOINT_URL")

# Request headers
headers = {
    "Content-Type": "application/json"
}

# Request body
data = {
    "messages": [
        {
            "role": "user",
            "content": "What is the indian news today in AI?"
        }
    ],
    "model": "claude-sonnet-4-5",
    "max_tokens": 4096
}

# Make the request
try:
    response = requests.post(endpoint_url, headers=headers, json=data)
    response.raise_for_status()  # Raise an error for bad status codes

    # Parse and print the response
    result = response.json()
    print(json.dumps(result, indent=2))

except requests.exceptions.RequestException as e:
    print(f"Error making request: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"Response status code: {e.response.status_code}")
        print(f"Response body: {e.response.text}")

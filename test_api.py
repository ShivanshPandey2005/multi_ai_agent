import requests
import json

url = "http://localhost:8000/ask"
payload = {"query": "What is LangChain and why is it useful?"}
headers = {"Content-Type": "application/json"}

print(f"Sending request to {url} with query: '{payload['query']}'...")
try:
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("\n--- [API Response] ---")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"\nError: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"\nConnection Error: {e}")

import requests

token = "update-token-here"
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("https://huggingface.co/api/whoami", headers=headers)

if response.status_code == 200:
    print(f"Valid token. User: {response.json().get('name')}")
else:
    print(f"Invalid token. Status: {response.status_code}, Error: {response.text}")

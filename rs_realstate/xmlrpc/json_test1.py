import requests

url = "http://127.0.0.1:8069/api/estate/properties/available/http"
response = requests.get(url)
response.raise_for_status()

data = response.json()
print("Total:", data["count"])

for prop in data["results"]:
    print(f"- {prop['name']} | {prop['state']} | {prop['expected_price']}")
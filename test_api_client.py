import requests

url = "http://127.0.0.1:9001/weather"

headers = {
    "X-API-Key": "ckfXuXcM97dOkZOFUnE9QnrxP_tz4rug6nltZnouwrs"
}

params = {
    "data_type": "current",
    "parameters": "temperature_c,humidity_percent,rainfall_mm",
    "limit": 5
}

response = requests.get(
    url,
    headers=headers,
    params=params
)

print("Status Code:", response.status_code)
print("Response:", response.json())
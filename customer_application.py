import requests

# Company's API URL
company_api_url = "http://127.0.0.1:9001/weather"

# Customer's API key
headers = {
    "X-API-Key": "ckfXuXcM97dOkZOFUnE9QnrxP_tz4rug6nltZnouwrs"
}

# Customer requests only these parameters
params = {
    "data_type": "current",
    "parameters": "temperature_c,humidity_percent",
    "limit": 1
}

# Send request to company's API
response = requests.get(
    company_api_url,
    headers=headers,
    params=params
)

# Display received data
if response.status_code == 200:
    weather_data = response.json()

    print("Customer Application")
    print("--------------------")
    print("API Status:", response.status_code)

    for record in weather_data["data"]:
        print("City:", record["city"])
        print("Temperature:", record["temperature_c"], "°C")
        print("Humidity:", record["humidity_percent"], "%")

else:
    print("API Request Failed:", response.status_code)
    print(response.text)
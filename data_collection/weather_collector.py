import requests

# Chennai location
LATITUDE = 13.0827
LONGITUDE = 80.2707

# Open-Meteo API
API_URL = "https://api.open-meteo.com/v1/forecast"

# Weather parameters
HOURLY_FIELDS = (
    "temperature_2m,"
    "relative_humidity_2m,"
    "wind_speed_10m,"
    "wind_direction_10m,"
    "precipitation,"
    "cloud_cover,"
    "weather_code"
)


def fetch_weather_data():

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": HOURLY_FIELDS,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m,"
            "wind_direction_10m,"
            "precipitation,"
            "cloud_cover,"
            "weather_code"
        ),
        "past_days": 7,
        "forecast_days": 5,
        "timezone": "Asia/Kolkata"
    }

    try:
        response = requests.get(
            API_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        print("Weather data collected successfully!")

        return data

    except requests.RequestException as error:

        print("Weather data collection failed:", error)

        return None


if __name__ == "__main__":

    weather_data = fetch_weather_data()

    if weather_data:

        print("\nCurrent Weather:")
        print(weather_data.get("current"))

        print("\nHourly Records:")
        print(len(weather_data["hourly"]["time"]))
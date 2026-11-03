from datetime import datetime
from zoneinfo import ZoneInfo


CITY = "Chennai"
TIMEZONE = ZoneInfo("Asia/Kolkata")


def process_weather_data(data):

    processed_records = []

    # Get current time from API response
    current_data = data.get("current")

    if current_data:
        current_time = datetime.fromisoformat(current_data["time"])

        current_record = {
            "city": CITY,
            "recorded_at": current_time,
            "data_type": "current",
            "temperature_c": current_data.get("temperature_2m"),
            "humidity_percent": current_data.get("relative_humidity_2m"),
            "wind_speed_kmh": current_data.get("wind_speed_10m"),
            "wind_direction_degrees": current_data.get("wind_direction_10m"),
            "rainfall_mm": current_data.get("precipitation"),
            "cloud_cover_percent": current_data.get("cloud_cover"),
            "weather_code": current_data.get("weather_code")
        }

        processed_records.append(current_record)

    # Get hourly data
    hourly_data = data.get("hourly", {})
    hourly_times = hourly_data.get("time", [])

    # Identify historical and forecast records
    current_time = datetime.now(TIMEZONE).replace(tzinfo=None)

    for index, time_value in enumerate(hourly_times):

        recorded_time = datetime.fromisoformat(time_value)

        if recorded_time <= current_time:
            data_type = "historical"
        else:
            data_type = "forecast"

        record = {
            "city": CITY,
            "recorded_at": recorded_time,
            "data_type": data_type,
            "temperature_c": hourly_data["temperature_2m"][index],
            "humidity_percent": hourly_data["relative_humidity_2m"][index],
            "wind_speed_kmh": hourly_data["wind_speed_10m"][index],
            "wind_direction_degrees": hourly_data["wind_direction_10m"][index],
            "rainfall_mm": hourly_data["precipitation"][index],
            "cloud_cover_percent": hourly_data["cloud_cover"][index],
            "weather_code": hourly_data["weather_code"][index]
        }

        processed_records.append(record)

    return processed_records
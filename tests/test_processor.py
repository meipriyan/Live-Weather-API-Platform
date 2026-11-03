from data_collection.weather_collector import fetch_weather_data
from data_collection.data_processor import process_weather_data


# Step 1: Collect weather data
weather_data = fetch_weather_data()

if weather_data:

    # Step 2: Process the collected data
    processed_records = process_weather_data(weather_data)

    # Step 3: Display the results
    print("\nData Processing Successful!")

    print("Total records:", len(processed_records))

    # Count each data type
    historical_count = 0
    forecast_count = 0
    current_count = 0

    for record in processed_records:

        if record["data_type"] == "historical":
            historical_count += 1

        elif record["data_type"] == "forecast":
            forecast_count += 1

        elif record["data_type"] == "current":
            current_count += 1

    print("\nHistorical records:", historical_count)
    print("Forecast records:", forecast_count)
    print("Current records:", current_count)

    # Display one sample record
    print("\nSample Processed Record:")
    print(processed_records[0])

else:
    print("No weather data available for processing.")
from data_collection.weather_collector import fetch_weather_data
from data_collection.data_processor import process_weather_data

from backend.weather_storage import save_weather_records
from backend.database import engine

from sqlalchemy import text


# Step 1: Collect weather data
weather_data = fetch_weather_data()

if weather_data:

    # Step 2: Process weather data
    processed_records = process_weather_data(weather_data)

    print("\nData processing completed!")
    print("Total records:", len(processed_records))

    # Step 3: Save records in MySQL
    save_weather_records(processed_records)

    # Step 4: Verify database records
    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT data_type, COUNT(*)
                FROM weather_records
                GROUP BY data_type
            """)
        )

        print("\nRecords available in MySQL:")

        for row in result:
            print(row[0], ":", row[1])

else:
    print("Weather data collection failed.")
from apscheduler.schedulers.blocking import BlockingScheduler

from data_collection.weather_collector import fetch_weather_data
from data_collection.data_processor import process_weather_data
from backend.weather_storage import save_weather_records


def update_weather_data():
    print("\nStarting automatic weather update...")

    weather_data = fetch_weather_data()

    if weather_data:
        processed_records = process_weather_data(weather_data)

        save_weather_records(processed_records)

        print("Automatic weather update completed!")

    else:
        print("Weather update failed!")


scheduler = BlockingScheduler()


scheduler.add_job(
    update_weather_data,
    trigger="interval",
    minutes=5
)


if __name__ == "__main__":
    print("Weather Scheduler Started!")
    print("Automatic update interval: Every 5 minutes")

    update_weather_data()

    scheduler.start()
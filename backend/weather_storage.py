from sqlalchemy.dialects.mysql import insert

from backend.database import SessionLocal
from backend.models import WeatherRecord


def save_weather_records(records):

    db = SessionLocal()

    try:
        saved_count = 0

        for record in records:

            statement = insert(WeatherRecord).values(**record)

            statement = statement.on_duplicate_key_update(
                temperature_c=statement.inserted.temperature_c,
                humidity_percent=statement.inserted.humidity_percent,
                wind_speed_kmh=statement.inserted.wind_speed_kmh,
                wind_direction_degrees=statement.inserted.wind_direction_degrees,
                rainfall_mm=statement.inserted.rainfall_mm,
                cloud_cover_percent=statement.inserted.cloud_cover_percent,
                weather_code=statement.inserted.weather_code
            )

            db.execute(statement)
            saved_count += 1

        db.commit()

        print("Weather records saved successfully!")
        print("Records processed:", saved_count)

    except Exception as error:
        db.rollback()
        print("Database storage failed!")
        print("Error:", error)

    finally:
        db.close()
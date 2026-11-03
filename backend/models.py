from sqlalchemy import Column, Integer, String, DateTime, Boolean, DECIMAL
from sqlalchemy.sql import func

from backend.database import Base


# Weather Records Table
class WeatherRecord(Base):

    __tablename__ = "weather_records"

    id = Column(Integer, primary_key=True, autoincrement=True)

    city = Column(String(100), nullable=False)

    recorded_at = Column(DateTime, nullable=False)

    data_type = Column(String(20), nullable=False)

    temperature_c = Column(DECIMAL(6, 2))

    humidity_percent = Column(DECIMAL(6, 2))

    wind_speed_kmh = Column(DECIMAL(6, 2))

    wind_direction_degrees = Column(DECIMAL(6, 2))

    rainfall_mm = Column(DECIMAL(8, 2))

    cloud_cover_percent = Column(DECIMAL(6, 2))

    weather_code = Column(Integer)


# Customers Table
class Customer(Base):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)

    customer_name = Column(String(150), nullable=False)

    api_key = Column(String(255), unique=True, nullable=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime,
        server_default=func.current_timestamp()
    )

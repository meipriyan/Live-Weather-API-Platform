
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.authentication import verify_api_key
from backend.database import get_db
from backend.models import WeatherRecord
from fastapi.responses import StreamingResponse

import csv
import io


# Create FastAPI application
app = FastAPI(
    title="Live Weather Data API",
    description="Company-managed weather data API",
    version="1.0"
)


# Parameters customers are allowed to request
AVAILABLE_PARAMETERS = {
    "temperature_c": WeatherRecord.temperature_c,
    "humidity_percent": WeatherRecord.humidity_percent,
    "wind_speed_kmh": WeatherRecord.wind_speed_kmh,
    "wind_direction_degrees": WeatherRecord.wind_direction_degrees,
    "rainfall_mm": WeatherRecord.rainfall_mm,
    "cloud_cover_percent": WeatherRecord.cloud_cover_percent,
    "weather_code": WeatherRecord.weather_code
}


@app.get("/")
def home():
    return {
        "message": "Welcome to Live Weather Data API",
        "status": "API is running"
    }


# JSON Weather Data API
@app.get("/weather")
def get_weather(
    data_type: str = "current",
    parameters: str = "temperature_c",
    limit: int = 100,
    db: Session = Depends(get_db),
    customer=Depends(verify_api_key)
):

    # Check requested data type
    allowed_types = ["current", "historical", "forecast"]

    if data_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Invalid data type"
        )

    # Convert requested parameters into a list
    requested_parameters = [
        parameter.strip()
        for parameter in parameters.split(",")
    ]

    # Validate requested parameters
    for parameter in requested_parameters:

        if parameter not in AVAILABLE_PARAMETERS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported parameter: {parameter}"
            )
   
    # Check limit
    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 1000"
        )

    # Current data should return only the latest record
    if data_type == "current":
        limit = 1

    # Retrieve records from MySQL
    records = (
        db.query(WeatherRecord)
        .filter(WeatherRecord.data_type == data_type)
        .order_by(WeatherRecord.recorded_at.desc())
        .limit(limit)
        .all()
    )

    # Prepare response with only requested parameters
    response = []

    for record in records:

        weather_item = {
            "city": record.city,
            "recorded_at": record.recorded_at,
            "data_type": record.data_type
        }

        for parameter in requested_parameters:
            weather_item[parameter] = getattr(record, parameter)

        response.append(weather_item)

    return {
        "total_records": len(response),
        "requested_data_type": data_type,
        "requested_parameters": requested_parameters,
        "data": response
    }


# CSV Weather Data Download API
@app.get("/weather/download")
def download_weather_csv(
    data_type: str = "current",
    parameters: str = "temperature_c",
    limit: int = 100,
    db: Session = Depends(get_db),
    customer=Depends(verify_api_key)
):

    # Check requested data type
    allowed_types = ["current", "historical", "forecast"]

    if data_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Invalid data type"
        )

    # Convert requested parameters into a list
    requested_parameters = [
        parameter.strip()
        for parameter in parameters.split(",")
    ]

    # Validate requested parameters
    for parameter in requested_parameters:

        if parameter not in AVAILABLE_PARAMETERS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported parameter: {parameter}"
            )
    
    # Check limit
    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 1000"
        )

    # Current data should return only the latest record
    if data_type == "current":
        limit = 1

    # Retrieve records from MySQL
    records = (
        db.query(WeatherRecord)
        .filter(WeatherRecord.data_type == data_type)
        .order_by(WeatherRecord.recorded_at.desc())
        .limit(limit)
        .all()
    )

    # Create CSV data
    output = io.StringIO()
    writer = csv.writer(output)

    headers = ["city", "recorded_at", "data_type"] + requested_parameters
    writer.writerow(headers)

    for record in records:

        row = [
            record.city,
            record.recorded_at,
            record.data_type
        ]

        for parameter in requested_parameters:
            row.append(getattr(record, parameter))

        writer.writerow(row)

    output.seek(0)

    # Return CSV file to customer
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=weather_data.csv"
        }
    )

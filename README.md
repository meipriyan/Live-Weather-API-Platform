# Live Weather API Platform

A live weather data collection, processing, storage, and distribution platform built using Python, FastAPI, MySQL, and Streamlit.

## Project Overview

The Live Weather API Platform collects weather information from an external weather API, processes the collected data, stores it in a MySQL database, and makes selected weather information available to customers through a REST API.

Customers can request specific weather parameters and receive the requested information in JSON or CSV format using API-key authentication.

## Key Features

- External weather data collection using Open-Meteo
- Weather data processing and analysis using Python and Pandas
- MySQL database integration
- FastAPI-based REST API
- API-key-based customer authentication
- Customer-specific parameter requests
- JSON and CSV data delivery
- Streamlit dashboard for weather data visualization
- Scheduled data collection using APScheduler

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| API Server | Uvicorn |
| Database | MySQL |
| Database Integration | SQLAlchemy, PyMySQL |
| Data Processing | Pandas |
| Frontend | Streamlit |
| Data Visualization | Plotly |
| Scheduler | APScheduler |
| External Data Source | Open-Meteo |

## Project Architecture

1. **Data Collection:** Retrieves weather information from Open-Meteo.
2. **Data Processing:** Processes and prepares the collected weather data.
3. **Database Storage:** Stores the processed information in MySQL.
4. **Backend API:** FastAPI provides endpoints to access weather information.
5. **Authentication:** Validates customer API keys.
6. **Customer Requests:** Customers specify the weather parameters they need.
7. **Data Delivery:** Returns requested information in JSON or CSV format.
8. **Dashboard:** Streamlit displays weather information through a user interface.

## Project Structure

```text
Live_Weather_API_Platform/
│
├── backend/
│   ├── authentication.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── scheduler.py
│   ├── test_connection.py
│   └── weather_storage.py
│
├── data_collection/
│   ├── data_processor.py
│   └── weather_collector.py
│
├── frontend/
│   └── app.py
│
├── tests/
│   ├── test_processor.py
│   └── test_storage.py
│
├── customer_application.py
├── test_api_client.py
├── requirements.txt
├── weather_download.csv
└── .gitignore
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/meipriyan/Live-Weather-API-Platform.git
```

### 2. Navigate to the project directory

```bash
cd Live-Weather-API-Platform
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure environment variables

Create a `.env` file in the project root directory.

Configure the database connection details required by the application. Do not upload real credentials or secrets to GitHub.

### 7. Start the backend API

```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 9001
```

### 8. Access API documentation

Open:

```text
http://127.0.0.1:9001/docs
```

### 9. Start the Streamlit dashboard

Open another terminal and run:

```bash
python -m streamlit run frontend/app.py --server.address 0.0.0.0 --server.port 8501
```

Access the dashboard at:

```text
http://127.0.0.1:8501
```

## API Usage

The platform provides weather data through its FastAPI backend.

Example endpoint:

```text
GET /weather
```

Customer authentication uses the following HTTP header:

```text
X-API-Key: YOUR_API_KEY
```

Customers can specify the parameters they need through request parameters.

The API supports JSON and CSV data delivery.

## Testing

The project includes test scripts for:

- Data processing
- Database storage
- Database connectivity
- Customer API requests

## Security

- API-key-based customer authentication
- Database credentials managed through environment variables
- `.env` and virtual environment excluded from version control

## Future Improvements

- Cloud deployment
- Enhanced customer access management
- Improved API monitoring and logging
- Additional data sources
- Improved automated testing

## Author

**MEIPRIYAN P**

B.Tech – Artificial Intelligence and Data Science

GitHub: [@meipriyan](https://github.com/meipriyan)
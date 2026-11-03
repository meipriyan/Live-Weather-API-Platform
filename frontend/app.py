
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv
# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Live Weather Analytics Platform",
    page_icon="🌤️",
    layout="wide"
)

st_autorefresh(
    interval=60 * 1000,
    key="weather_dashboard_refresh"
)

load_dotenv()

API_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
).rstrip("/")
# --------------------------------------------------
# BLACK AND DARK ORANGE THEME
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #101010;
    color: #F5F5F5;
}

[data-testid="stSidebar"] {
    background-color: #191919;
    border-right: 1px solid #333333;
}

h1, h2, h3 {
    color: #FF8C00 !important;
}

p, label, span {
    color: #E5E5E5;
}

div[data-testid="stMetric"] {
    background-color: #202020;
    border: 1px solid #FF8C00;
    padding: 18px;
    border-radius: 12px;
}

div[data-testid="stMetricLabel"] {
    color: #FFB347 !important;
}

div[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
}

.stButton > button {
    background-color: #FF8C00;
    color: #111111;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    padding: 10px 20px;
}

.stButton > button:hover {
    background-color: #FFA500;
    color: #000000;
    border: 1px solid #FFFFFF;
}

div[data-testid="stDownloadButton"] button {
    background-color: #FF8C00;
    color: #111111;
    font-weight: bold;
}

hr {
    border-color: #444444;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
div[data-testid="stMetricLabel"] {
    font-size: 14px !important;
}

div[data-testid="stMetricValue"] {
    font-size: 24px !important;
    white-space: nowrap !important;
}

div[data-testid="stMetric"] {
    min-width: 0;
    padding: 12px;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# DASHBOARD HEADER
# --------------------------------------------------

st.title("🌤️ LIVE WEATHER ANALYTICS")
st.caption("Company-Managed Live Weather Data Platform")

st.markdown(
    "Monitor, analyse and access selected weather parameters "
    "through our secure company API."
)

st.markdown("---")


# --------------------------------------------------
# SIDEBAR - CUSTOMER ACCESS
# --------------------------------------------------

st.sidebar.title("⚙️ CUSTOMER PANEL")
st.sidebar.markdown("---")

api_key = st.sidebar.text_input(
    "Enter Your API Key",
    type="password"
)

st.sidebar.markdown("---")

st.sidebar.subheader("Data Request Settings")

data_type = st.sidebar.selectbox(
    "Select Data Type",
    ["current", "historical", "forecast"],
    key="weather_data_type"
)

parameters_list = [
    "temperature_c",
    "humidity_percent",
    "wind_speed_kmh",
    "wind_direction_degrees",
    "rainfall_mm",
    "cloud_cover_percent",
    "weather_code"
]

selected_parameters = st.sidebar.multiselect(
    "Select Weather Parameters",
    parameters_list,
    default=["temperature_c"],
    key="weather_parameters"
)

limit = st.sidebar.number_input(
    "Number of Records",
    min_value=1,
    max_value=1000,
    value=100,
    key="weather_record_limit"
)

st.sidebar.markdown("---")
st.sidebar.caption("Secure API Access | Chennai Weather Data")


# --------------------------------------------------
# HELPER FUNCTION FOR CHARTS
# --------------------------------------------------

def create_weather_chart(dataframe, parameter):

    chart_data = dataframe[
        ["recorded_at", parameter]
    ].dropna()

    if chart_data.empty:
        st.info("No values available for this parameter.")
        return

    chart_data["recorded_at"] = pd.to_datetime(
        chart_data["recorded_at"]
    )

    
    chart_titles = {
        "temperature_c": "Temperature (°C)",
        "humidity_percent": "Humidity (%)",
        "wind_speed_kmh": "Wind Speed (km/h)",
        "wind_direction_degrees": "Wind Direction (°)",
        "rainfall_mm": "Rainfall (mm)",
        "cloud_cover_percent": "Cloud Cover (%)",
        "weather_code": "Weather Code"
    }

    title = chart_titles.get(
        parameter,
        parameter.replace("_", " ").title()
    )


    if parameter == "rainfall_mm":

        figure = px.bar(
            chart_data,
            x="recorded_at",
            y=parameter,
            title=title,
            color_discrete_sequence=["#FF8C00"]
        )

    else:

        figure = px.line(
            chart_data,
            x="recorded_at",
            y=parameter,
            title=title,
            markers=True,
            color_discrete_sequence=["#FF8C00"]
        )

    figure.update_layout(
        template="plotly_dark",
        paper_bgcolor="#202020",
        plot_bgcolor="#202020",
        font_color="white",
        title_font_color="#FF8C00",
        xaxis_title="Date and Time",
        yaxis_title=title,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(
        figure,
        use_container_width=True
    )


# --------------------------------------------------
# GET WEATHER DATA
# --------------------------------------------------

st.subheader("📊 Weather Data Request")

if st.button("🔍 Get Weather Data", use_container_width=True):

    if not api_key:
        st.error("Please enter your API key.")

    elif not selected_parameters:
        st.warning("Please select at least one parameter.")

    else:

        headers = {
            "X-API-Key": api_key
        }

        params = {
            "data_type": data_type,
            "parameters": ",".join(selected_parameters),
            "limit": limit
        }

        try:

            response = requests.get(
                f"{API_URL}/weather",
                headers=headers,
                params=params,
                timeout=30
            )

            if response.status_code == 200:

                result = response.json()

                st.success(
                    "Weather data retrieved successfully!"
                )

                st.markdown("---")

                st.subheader("📈 WEATHER DATA OVERVIEW")

                if result["data"]:

                    dataframe = pd.DataFrame(result["data"])

                    latest_record = result["data"][0]

                    

                    # DASHBOARD SUMMARY CARDS

                    summary_columns = st.columns(4)

                    with summary_columns[0]:
                        st.metric(
                            label="API STATUS",
                            value="CONNECTED"
                        )

                    with summary_columns[1]:
                        st.metric(
                            label="DATA TYPE",
                            value=result["requested_data_type"].upper()
                        )

                    with summary_columns[2]:
                        st.metric(
                            label="TOTAL RECORDS",
                            value=result["total_records"]
                        )

                    with summary_columns[3]:
                        st.metric(
                            label="LATEST RECORD",
                            value=str(latest_record["recorded_at"])[11:16]
                        )

                    # KPI CARDS

                    metric_parameters = [
                        parameter
                        for parameter in selected_parameters
                        if latest_record.get(parameter) is not None
                    ]

                    if metric_parameters:

                        columns = st.columns(
                            min(len(metric_parameters), 4)
                        )

                        for index, parameter in enumerate(
                            metric_parameters
                        ):

                            value = latest_record[parameter]

                            columns[index % 4].metric(
                                label=parameter.replace(
                                    "_", " "
                                ).title(),
                                value=value
                            )

                    st.markdown("---")

                    # CHARTS

                    st.subheader("📉 WEATHER ANALYTICS & CHARTS")

                    chart_parameters = [
                        parameter
                        for parameter in selected_parameters
                        if parameter in dataframe.columns
                        and pd.api.types.is_numeric_dtype(
                            dataframe[parameter]
                        )
                    ]

                    if chart_parameters:

                        for start in range(
                            0, len(chart_parameters), 2
                        ):

                            chart_columns = st.columns(2)

                            for index, parameter in enumerate(
                                chart_parameters[start:start + 2]
                            ):

                                with chart_columns[index]:

                                    create_weather_chart(
                                        dataframe,
                                        parameter
                                    )

                    else:

                        st.info(
                            "No numerical parameters selected for charts."
                        )

                    st.markdown("---")

                    # DATA TABLE

                    st.subheader("📋 RETRIEVED WEATHER RECORDS")

                    st.dataframe(
                        dataframe,
                        use_container_width=True,
                        hide_index=True
                    )

                else:

                    st.info("No weather records available.")

            else:

                st.error(
                    f"Request failed: {response.status_code}"
                )

                st.write(response.text)

        except requests.RequestException as error:

            st.error(f"Connection error: {error}")


# --------------------------------------------------
# CSV DOWNLOAD
# --------------------------------------------------

st.markdown("---")

st.subheader("📥 DOWNLOAD WEATHER DATA")

st.write(
    "Download the selected weather parameters "
    "as a CSV file."
)

if st.button("Prepare CSV Download", use_container_width=True):

    if not api_key:

        st.error("Please enter your API key.")

    elif not selected_parameters:

        st.warning("Please select at least one parameter.")

    else:

        headers = {
            "X-API-Key": api_key
        }

        params = {
            "data_type": data_type,
            "parameters": ",".join(selected_parameters),
            "limit": limit
        }

        try:

            response = requests.get(
                f"{API_URL}/weather/download",
                headers=headers,
                params=params,
                timeout=30
            )

            if response.status_code == 200:

                st.success("CSV file generated successfully!")

                st.download_button(
                    label="⬇️ Save Weather CSV",
                    data=response.content,
                    file_name="weather_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            else:

                st.error(
                    f"CSV download failed: {response.status_code}"
                )

                st.write(response.text)

        except requests.RequestException as error:

            st.error(f"Connection error: {error}")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Live Weather Analytics Platform | "
    "Powered by Python, FastAPI, MySQL and Streamlit"
)


# Structured India AQI Dashboard Code

import streamlit as st
import pandas as pd
import folium

from streamlit_folium import st_folium


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="India AQI Dashboard",
    layout="wide"
)


# =====================================================
# LOAD DATA
# =====================================================

dataset = pd.read_csv("air_quality_health_monthly.csv")


# =====================================================
# DATA PREPROCESSING
# =====================================================

# Create date column

dataset['date'] = pd.to_datetime(
    dataset['year'].astype(str) + '-' +
    dataset['month'].astype(str) + '-01'
)


# Latest AQI record for each city

latest_city_data = (
    dataset
    .sort_values('date')
    .groupby('city')
    .last()
    .reset_index()
)


# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.title("Filters")

city = st.sidebar.selectbox(
    "Select City",
    dataset['city'].unique()
)


# =====================================================
# FILTERED DATA
# =====================================================

filtered = dataset[
    dataset['city'] == city
].copy()

filtered = filtered.sort_values('date')


# =====================================================
# AQI CATEGORY FUNCTION
# =====================================================


def get_aqi_category(aqi):

    if aqi <= 50:
        return "Good"

    elif aqi <= 100:
        return "Satisfactory"

    elif aqi <= 200:
        return "Moderate"

    elif aqi <= 300:
        return "Poor"

    elif aqi <= 400:
        return "Very Poor"

    else:
        return "Severe"


# =====================================================
# MAP MARKER COLOR FUNCTION
# =====================================================


def get_marker_color(aqi):

    if aqi <= 50:
        return "green"

    elif aqi <= 100:
        return "blue"

    elif aqi <= 200:
        return "orange"

    elif aqi <= 300:
        return "red"

    else:
        return "darkred"


# =====================================================
# DASHBOARD TITLE
# =====================================================

st.title("India AQI Dashboard")

st.write("Interactive Air Quality Monitoring Dashboard")


# =====================================================
# DATA PREVIEW
# =====================================================

st.subheader("Dataset Preview")

st.dataframe(dataset.head())


# =====================================================
# OVERALL METRICS
# =====================================================

st.subheader("Overall AQI Overview")

st.metric(
    "Average AQI",
    round(dataset['aqi'].mean(), 2)
)


# =====================================================
# OVERALL AQI TREND
# =====================================================

st.line_chart(
    dataset.set_index('date')['aqi']
)


# =====================================================
# CURRENT CITY AQI
# =====================================================

latest_aqi = filtered['aqi'].iloc[-1]

category = get_aqi_category(latest_aqi)

st.subheader(f"Current AQI Status - {city}")

st.metric(
    "Current AQI",
    round(latest_aqi, 2)
)

st.write("AQI Category:", category)


# =====================================================
# KPI CARDS
# =====================================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average AQI",
    round(filtered['aqi'].mean(), 2)
)

col2.metric(
    "Maximum AQI",
    round(filtered['aqi'].max(), 2)
)

col3.metric(
    "Minimum AQI",
    round(filtered['aqi'].min(), 2)
)


# =====================================================
# CITY AQI TREND
# =====================================================

st.subheader(f"AQI Trend - {city}")

st.line_chart(
    filtered.set_index('date')['aqi']
)


# =====================================================
# POLLUTANT ANALYSIS
# =====================================================

pollutants = filtered[
    [
        'pm25_ug_m3',
        'pm10_ug_m3',
        'no2_ug_m3'
    ]
]

st.subheader("Pollutant Levels")

st.line_chart(pollutants)


# =====================================================
# HEALTH IMPACT ANALYSIS
# =====================================================

health = filtered[
    [
        'respiratory_admissions_per_100k',
        'asthma_er_visits_per_100k'
    ]
]

st.subheader("Health Impact")

st.line_chart(health)


# =====================================================
# GIS AQI MAP
# =====================================================

st.subheader("India AQI Map")
st.write("Air Quality Monitoring System")

m = folium.Map(
    location=[22, 80],
    zoom_start=5
)


# Add AQI markers

for index, row in latest_city_data.iterrows():

    folium.CircleMarker(

        location=[
            row['latitude'],
            row['longitude']
        ],

        radius=8,

        popup=f"""
        City: {row['city']} <br>
        AQI: {row['aqi']} <br>
        PM2.5: {row['pm25_ug_m3']}
        """,

        color=get_marker_color(row['aqi']),

        fill=True,
        fill_opacity=0.7

    ).add_to(m)


# Display map

st_folium(
    m,
    width=1000,
    height=500
)


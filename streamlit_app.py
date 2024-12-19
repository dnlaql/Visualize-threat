import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Dataset URL
DATA_URL = "https://raw.githubusercontent.com/dnlaql/Visualize-threat/refs/heads/main/dataset/threat%20(1).csv"

# Load the dataset
@st.cache_data
def load_data(url):
    """Loads and processes the dataset."""
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()  # Clean column names
        df['Time Detected'] = pd.to_datetime(df['Time Detected'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data(DATA_URL)

# Filter function
def filter_data(df, threat_type=None, start_date=None, end_date=None, engine=None):
    """Filters the dataset based on selected criteria."""
    if threat_type and threat_type != "All":
        df = df[df['Type'] == threat_type]
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        df = df[(df['Time Detected'] >= start_date) & (df['Time Detected'] <= end_date)]
    if engine and engine != "All":
        df = df[df['Engine'] == engine]
    return df

# Sidebar Filters
st.sidebar.header("Filters")

# Initialize filter states
if "filters" not in st.session_state:
    st.session_state.filters = {
        "threat_type": "All",
        "start_date": df['Time Detected'].min(),
        "end_date": df['Time Detected'].max(),
        "engine": "All",
    }

# Display filters
threat_type = st.sidebar.selectbox(
    "Select Threat Type", options=["All"] + list(df['Type'].unique()), index=0
)
start_date = st.sidebar.date_input("Start Date", st.session_state.filters["start_date"])
end_date = st.sidebar.date_input("End Date", st.session_state.filters["end_date"])
engine = st.sidebar.selectbox(
    "Select Engine", options=["All"] + list(df['Engine'].unique()), index=0
)

# Search Button
if st.sidebar.button("Search"):
    st.session_state.filters = {
        "threat_type": threat_type,
        "start_date": start_date,
        "end_date": end_date,
        "engine": engine,
    }
    df_filtered = filter_data(
        df,
        threat_type=st.session_state.filters["threat_type"],
        start_date=st.session_state.filters["start_date"],
        end_date=st.session_state.filters["end_date"],
        engine=st.session_state.filters["engine"],
    )
else:
    df_filtered = filter_data(
        df,
        threat_type=st.session_state.filters["threat_type"],
        start_date=st.session_state.filters["start_date"],
        end_date=st.session_state.filters["end_date"],
        engine=st.session_state.filters["engine"],
    )

# Reset Filters Button
if st.sidebar.button("Reset Filters"):
    st.session_state.filters = {
        "threat_type": "All",
        "start_date": df['Time Detected'].min(),
        "end_date": df['Time Detected'].max(),
        "engine": "All",
    }
    df_filtered = df  # Reset to full dataset

# Exploratory Data Analysis (EDA)

# 1. Distribution of Threat Types
st.write("### Distribution of Threat Types")
# Description: Shows the frequency of different threat types detected
threat_type_counts = df_filtered['Type'].value_counts()
st.bar_chart(threat_type_counts)

# 2. Time Series of Threat Detection
st.write("### Time Series of Threat Detection")
# Description: Displays how threats were detected over time
time_detected = df_filtered.groupby(df_filtered['Time Detected'].dt.date).size()
st.line_chart(time_detected)

# 3. Antivirus Engine Effectiveness
st.write("### Antivirus Engine Effectiveness")
# Description: Shows the detection results grouped by engine and status
engine_threat_counts = df_filtered.groupby('Engine')['Status'].value_counts().unstack().fillna(0)
st.bar_chart(engine_threat_counts)

# 4. Resolution Time Analysis (New EDA)
st.write("### Resolution Time Analysis by Engine")
# Description: Average time taken by each engine to resolve the threat
df_filtered['Resolution Time'] = (df_filtered['Time Fixed'] - df_filtered['Time Created']).dt.total_seconds() / 3600  # Resolution time in hours
avg_resolution_time = df_filtered.groupby('Engine')['Resolution Time'].mean().sort_values(ascending=False)
st.bar_chart(avg_resolution_time)

# 5. Trend of Resolution Time Over Time
st.write("### Resolution Time Trend Over Time")
# Description: Displays the trend of average resolution time over time
df_filtered['Resolution Time Date'] = df_filtered['Time Created'].dt.date
resolution_time_trend = df_filtered.groupby('Resolution Time Date')['Resolution Time'].mean()
st.line_chart(resolution_time_trend)

# 6. Outliers: Long Resolution Times
st.write("### Outlier Detection (Long Resolution Times)")
# Description: Identifies threats with unusually long resolution times (Top 5%)
outliers = df_filtered[df_filtered['Resolution Time'] > df_filtered['Resolution Time'].quantile(0.95)]  # Top 5% as outliers
st.write(outliers[['Endpoint', 'Resolution Time', 'Time Created', 'Time Fixed', 'Engine']])


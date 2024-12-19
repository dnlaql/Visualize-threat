import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Dataset URL
DATA_URL = "https://raw.githubusercontent.com/dnlaql/Visualize-threat/refs/heads/main/dataset/threat%20(1).csv"

# Load the dataset
@st.cache_data
def load_data(url):
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()  # Remove leading/trailing spaces from column names
        df['Time Detected'] = pd.to_datetime(df['Time Detected'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data(DATA_URL)

# Filter function
def filter_data(df, threat_type=None, start_date=None, end_date=None, engine=None):
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

# Explore Data Analysis Insight

# 1. Distribution of Threat Types
st.write("### Distribution of Threat Types")
threat_type_counts = df_filtered['Type'].value_counts()
st.bar_chart(threat_type_counts)

# 2. Time Series of Threat Detection
st.write("### Time Series of Threat Detection")
time_detected = df_filtered.groupby(df_filtered['Time Detected'].dt.date).size()
st.line_chart(time_detected)

# 3. Antivirus Engine Effectiveness
st.write("### Antivirus Engine Effectiveness")
engine_threat_counts = df_filtered.groupby('Engine')['Status'].value_counts().unstack().fillna(0)
st.bar_chart(engine_threat_counts)

# 4. Engine Performance: Compare the number of threats detected by each engine
st.write("### Engine Performance")
engine_performance = df_filtered['Engine'].value_counts()
st.bar_chart(engine_performance)

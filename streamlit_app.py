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
    if threat_type:
        df = df[df['Threat'] == threat_type]
    if start_date and end_date:
        df = df[(df['Time Detected'] >= start_date) & (df['Time Detected'] <= end_date)]
    if engine:
        df = df[df['Engine'] == engine]
    return df

# Placeholder for selecting filters
st.sidebar.header("Filters")
threat_type = st.sidebar.selectbox("Select Threat Type", options=df['Threat'].unique(), index=0)
start_date = st.sidebar.date_input("Start Date", df['Time Detected'].min())
end_date = st.sidebar.date_input("End Date", df['Time Detected'].max())
engine = st.sidebar.selectbox("Select Engine", options=df['Engine'].unique(), index=0)

df_filtered = filter_data(df, threat_type, start_date, end_date, engine)

# 1. Distribution of Threat Types
st.write("Distribution of Threat Types")
threat_type_counts = df_filtered['Threat'].value_counts()
st.bar_chart(threat_type_counts)

# 2. Time Series of Threat Detection
st.write("Time Series of Threat Detection")
time_detected = df_filtered.groupby(df_filtered['Time Detected'].dt.date).size()
st.line_chart(time_detected)

# 3. Department vs Threat Type (Grouped by IP Address)
st.write("IP Address vs Threat Type")
ip_threat_counts = df_filtered.groupby(['IP Address', 'Threat']).size().unstack().fillna(0)
st.bar_chart(ip_threat_counts)

# 4. Antivirus Engine Effectiveness
st.write("Antivirus Engine Effectiveness")
engine_threat_counts = df_filtered.groupby('Engine')['Status'].value_counts().unstack().fillna(0)
st.bar_chart(engine_threat_counts)

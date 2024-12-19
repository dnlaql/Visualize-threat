#---------------------------------------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
#---------------------------------------------------------------------------------------------------------

# Dataset URL
DATA_URL = "https://raw.githubusercontent.com/dnlaql/Visualize-threat/refs/heads/main/dataset/threat%20(1).csv"

#---------------------------------------------------------------------------------------------------------
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
#---------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------
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
threat_type = st.sidebar.selectbox("Select Threat Type", options=["All"] + list(df['Type'].unique()))
start_date = st.sidebar.date_input("Start Date", df['Time Detected'].min())
end_date = st.sidebar.date_input("End Date", df['Time Detected'].max())
engine = st.sidebar.selectbox("Select Engine", options=["All"] + list(df['Engine'].unique()))

#---------------------------------------------------------------------------------------------------------
# Filter and Reset Buttons
reset_triggered = st.sidebar.button("Reset Filters")

if reset_triggered:
    threat_type = "All"
    start_date = df['Time Detected'].min()
    end_date = df['Time Detected'].max()
    engine = "All"
else:
    threat_type = st.sidebar.selectbox("Select Threat Type", options=["All"] + list(df['Type'].unique()))
    start_date = st.sidebar.date_input("Start Date", df['Time Detected'].min())
    end_date = st.sidebar.date_input("End Date", df['Time Detected'].max())
    engine = st.sidebar.selectbox("Select Engine", options=["All"] + list(df['Engine'].unique()))

df_filtered = filter_data(df, threat_type, start_date, end_date, engine)
#---------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------
# EXPLORE DATA ANALYSIS INSIGHT
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
#---------------------------------------------------------------------------------------------------------

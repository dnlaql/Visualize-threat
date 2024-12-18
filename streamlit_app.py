import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Dataset URL
DATA_URL = "https://raw.githubusercontent.com/dnlaql/Visualize-threat/refs/heads/main/dataset/threat%20(1).csv"

# Load the dataset
@st.cache_data
def load_data(url):
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()  # Remove leading/trailing spaces from column names
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data(DATA_URL)

# Filter function
def filter_data(df, threat_type=None, engine=None):
    if threat_type:
        df = df[df['Threat'] == threat_type]
    if engine:
        df = df[df['Engine'] == engine]
    return df

# Placeholder for selecting filters
st.sidebar.header("Filters")
threat_type = st.sidebar.selectbox("Select Threat Type", options=df['Threat'].unique(), index=0)
engine = st.sidebar.selectbox("Select Engine", options=df['Engine'].unique(), index=0)

df_filtered = filter_data(df, threat_type, engine)

# 1. Distribution of Threat Types
st.write("Distribution of Threat Types")
threat_type_counts = df_filtered['Threat'].value_counts()
st.bar_chart(threat_type_counts)

# 2. Time Series of Threat Detection
st.write("Time Series of Threat Detection")
df_filtered['Time Detected'] = pd.to_datetime(df_filtered['Time Detected'], errors='coerce')
time_detected = df_filtered.groupby(df_filtered['Time Detected'].dt.date).size()
st.line_chart(time_detected)

# 3. Department vs Threat Type (Stacked Bar Chart)
st.write("Department vs Threat Type")
# Here, we'll show the distribution of threats per IP address instead of department
department_threat_counts = df_filtered.groupby(['IP Address', 'Threat']).size().unstack().fillna(0)
st.bar_chart(department_threat_counts)

# 4. Antivirus Engine Effectiveness
st.write("Antivirus Engine Effectiveness")
engine_threat_counts = df_filtered.groupby('Engine')['Status'].value_counts().unstack().fillna(0)
st.bar_chart(engine_threat_counts)

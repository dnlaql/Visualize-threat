import streamlit as st
import pandas as pd

# Load your data
@st.cache
def load_data():
    data = pd.read_csv('path_to_your_file.csv')
    data['Time Detected'] = pd.to_datetime(data['Time Detected'])
    return data

df = load_data()

# Sidebar for filters
st.sidebar.header('Filters')
date_range = st.sidebar.date_input("Date range", [])
department = st.sidebar.multiselect('Department', options=df['Department'].unique())
threat_type = st.sidebar.multiselect('Type', options=df['Type'].unique())
status = st.sidebar.multiselect('Status', options=df['Status'].unique())
engine = st.sidebar.multiselect('Engine', options=df['Engine'].unique())

# Apply filters
df_filtered = df[(df['Department'].isin(department)) & 
                 (df['Type'].isin(threat_type)) & 
                 (df['Status'].isin(status)) & 
                 (df['Engine'].isin(engine))]

if date_range:
    df_filtered = df_filtered[(df_filtered['Time Detected'].dt.date >= date_range[0]) & 
                              (df_filtered['Time Detected'].dt.date <= date_range[1])]

# Dashboard Title
st.title('Threat Analysis Dashboard')

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

# Display filtered data
st.write("### Filtered Data", df_filtered)

import streamlit as st
import pandas as pd
import plotly.express as px

# Using st.cache_data for loading and caching data
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/dnlaql/Visualize-threat/refs/heads/main/dataset/updated_edr-threat_with_departments.csv'
    data = pd.read_csv(url)
    data['Time Detected'] = pd.to_datetime(data['Time Detected'])
    return data

df = load_data()

# Sidebar for user inputs and filters
st.sidebar.header('Filters')
date_range = st.sidebar.date_input("Date Range", [])
department = st.sidebar.selectbox('Department', ['All'] + sorted(df['Department'].unique()))
type_filter = st.sidebar.multiselect('Type', options=sorted(df['Type'].unique()))
status_filter = st.sidebar.multiselect('Status', options=sorted(df['Status'].unique()))
engine_filter = st.sidebar.multiselect('Engine', options=sorted(df['Engine'].unique()))

# Apply filters
conditions = True
if date_range:
    conditions &= (df['Time Detected'] >= date_range[0]) & (df['Time Detected'] <= date_range[1])
if department != 'All':
    conditions &= (df['Department'] == department)
if type_filter:
    conditions &= df['Type'].isin(type_filter)
if status_filter:
    conditions &= df['Status'].isin(status_filter)
if engine_filter:
    conditions &= df['Engine'].isin(engine_filter)

filtered_data = df[conditions]

# Main dashboard title and description
st.title('Threat Monitoring and Analysis Dashboard')
st.markdown("""
Welcome to the interactive Threat Monitoring Dashboard. This tool provides insights into network security threats detected over time, allowing for effective monitoring and decision-making based on detailed data-driven insights.
""")

# Distribution of Threat Types
fig = px.bar(filtered_data, x='Type', title="Distribution of Threat Types")
st.plotly_chart(fig, use_container_width=True)

# Time Series Analysis of Threat Detection
fig_time = px.line(filtered_data.groupby(filtered_data['Time Detected'].dt.date).size(), title='Threats Over Time')
st.plotly_chart(fig_time, use_container_width=True)

# Status of Threat Resolutions
fig_status = px.pie(filtered_data, names='Status', title='Status of Threat Resolutions')
st.plotly_chart(fig_status, use_container_width=True)

# Antivirus Engine Effectiveness
engine_status = filtered_data.groupby(['Engine', 'Status']).size().unstack().fillna(0)
fig_engine = px.bar(engine_status, barmode='group', title='Engine Effectiveness by Status')
st.plotly_chart(fig_engine, use_container_width=True)

# Display the filtered data
st.subheader("Filtered Data")
st.dataframe(filtered_data)

# Reset button to clear filters
if st.sidebar.button('Reset Filters'):
    st.experimental_rerun()

# Note on caching
st.info('Data is cached for performance. Adjust filters to view different slices of data.')

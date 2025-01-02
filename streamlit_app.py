import streamlit as st
import pandas as pd
import plotly.express as px

# Use st.cache_data for loading and caching data for better performance
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/dnlaql/Visualize-threat/refs/heads/main/dataset/updated_edr-threat_with_departments.csv'
    data = pd.read_csv(url)
    data['Time Detected'] = pd.to_datetime(data['Time Detected'])
    return data

df = load_data()

# Initialize session state variables if not already set
if 'date_range' not in st.session_state:
    st.session_state['date_range'] = []
if 'department' not in st.session_state:
    st.session_state['department'] = 'All'
if 'type_filter' not in st.session_state:
    st.session_state['type_filter'] = []
if 'status_filter' not in st.session_state:
    st.session_state['status_filter'] = []
if 'engine_filter' not in st.session_state:
    st.session_state['engine_filter'] = []

# Sidebar for filters
st.sidebar.header('Filters 🎚️')
date_range = st.sidebar.date_input("Date Range 📅", key='date_range')
department = st.sidebar.selectbox('Department 🏢', ['All'] + sorted(df['Department'].unique()), key='department')
type_filter = st.sidebar.multiselect('Type 🚨', options=sorted(df['Type'].unique()), key='type_filter')
status_filter = st.sidebar.multiselect('Status 📊', options=sorted(df['Status'].unique()), key='status_filter')
engine_filter = st.sidebar.multiselect('Engine 🖥️', options=sorted(df['Engine'].unique()), key='engine_filter')

def reset_filters():
    st.session_state['date_range'] = []
    st.session_state['department'] = 'All'
    st.session_state['type_filter'] = []
    st.session_state['status_filter'] = []
    st.session_state['engine_filter'] = []

# Button to reset filters
if st.sidebar.button('Reset Filters 🔄'):
    reset_filters()

# Apply filters to the data based on user selections
filtered_data = df.copy()
if date_range:
    filtered_data = filtered_data[(filtered_data['Time Detected'] >= date_range[0]) & (filtered_data['Time Detected'] <= date_range[1])]
if department != 'All':
    filtered_data = filtered_data[filtered_data['Department'] == department]
if type_filter:
    filtered_data = filtered_data[filtered_data['Type'].isin(type_filter)]
if status_filter:
    filtered_data = filtered_data[filtered_data['Status'].isin(status_filter)]
if engine_filter:
    filtered_data = filtered_data[filtered_data['Engine'].isin(engine_filter)]
# Dashboard title and introduction
st.title('Threat Monitoring and Analysis Dashboard 🛡️')
st.markdown("""
Welcome to the interactive Threat Monitoring Dashboard! This tool is designed to provide insights into network security threats detected over time, enhancing monitoring and decision-making processes.
""")

# EDA Insight Descriptions and Visualizations
## Distribution of Threat Types
st.subheader("Distribution of Threat Types 📊")
st.markdown("This bar chart visualizes the frequency of each threat type, highlighting the most prevalent threats that the organization faces.")
fig1 = px.bar(filtered_data, x='Type', title="Threat Types Distribution")
st.plotly_chart(fig1, use_container_width=True)

## Time Series Analysis of Threat Detection
st.subheader("Time Series Analysis of Threat Detection ⏳")
st.markdown("The line chart below tracks the number of threats detected over time, allowing users to identify trends and patterns in threat activity.")
fig2 = px.line(filtered_data.groupby(filtered_data['Time Detected'].dt.date).size(), title='Daily Threats')
st.plotly_chart(fig2, use_container_width=True)

## Status of Threat Resolutions
st.subheader("Status of Threat Resolutions 📈")
st.markdown("This pie chart breaks down the statuses of threat resolutions, providing insight into the effectiveness of the organization’s response strategies.")
status_counts = filtered_data['Status'].value_counts().reset_index()
status_counts.columns = ['Status', 'Count']
fig3 = px.pie(status_counts, values='Count', names='Status', title='Threat Resolution Status')
st.plotly_chart(fig3, use_container_width=True)

## Antivirus Engine Effectiveness
st.subheader("Antivirus Engine Effectiveness 🖥️")
st.markdown("Analyze how different antivirus engines perform in terms of threat detection and resolution. Each bar represents the performance of an engine against various threat statuses.")
engine_status = filtered_data.groupby(['Engine', 'Status']).size().unstack().fillna(0)
fig4 = px.bar(engine_status, barmode='group', title='Engine Effectiveness by Status')
st.plotly_chart(fig4, use_container_width=True)

# Display filtered data
st.subheader("Filtered Data Table 📝")
st.dataframe(filtered_data)

# Reset button to clear all filters
if st.sidebar.button('Reset Filters 🔄'):
    st.experimental_rerun()

# Footer note on data caching
st.info('Data is cached for performance. Adjust filters to view different slices of data.')

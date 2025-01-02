import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load data
@st.cache
def load_data():
    url = 'https://raw.githubusercontent.com/dnlaql/Visualize-threat/refs/heads/main/dataset/updated_edr-threat_with_departments.csv'
    data = pd.read_csv(url)
    data['Time Detected'] = pd.to_datetime(data['Time Detected'])  # Convert to datetime
    return data

df = load_data()

# Sidebar for user inputs and filters
st.sidebar.header('Filters')
date_range = st.sidebar.date_input("Date Range", [])
department = st.sidebar.selectbox('Department', ['All'] + sorted(df['Department'].unique()))
type_filter = st.sidebar.multiselect('Type', options=sorted(df['Type'].unique()))
status_filter = st.sidebar.multiselect('Status', options=sorted(df['Status'].unique()))
engine_filter = st.sidebar.multiselect('Engine', options=sorted(df['Engine'].unique()))

# Apply filters to data
conditions = [True] * len(df)  # Default to all true
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

# Main dashboard title
st.title('Threat Monitoring and Analysis Dashboard 🛡️')

# Description of the dashboard with emojis
st.markdown("""
Welcome to the Threat Monitoring and Analysis Dashboard! 🌍 This interactive tool provides a comprehensive overview 
of network security threats detected over time, helping IT security analysts to monitor, analyze, and respond to 
potential threats effectively. 🚀

**Features:**
- **Filter Data:** Users can dynamically filter the data based on date ranges, departments, threat types, statuses, 
and antivirus engines. 🔍
- **Visualizations Include:**
  - Distribution of threat types 📊
  - Time series analysis of threat detections ⏳
  - Status of threat resolutions 📈
  - Antivirus engine effectiveness 💻
  
**Usage:**
- Use the sidebar to apply different filters and interact with the visualizations. 🎛️
- Hover over graphs to see additional details or trends over time. 🔎

Feel free to explore and customize the views to gain better insights into the security landscape. 🌐
""")

# Distribution of Threat Types
st.subheader("Distribution of Threat Types")
fig = px.bar(filtered_data, x='Type', title="Threat Types Distribution")
st.plotly_chart(fig, use_container_width=True)

# Time Series of Threat Detection
st.subheader("Time Series of Threat Detection")
time_series = filtered_data.groupby(filtered_data['Time Detected'].dt.date).size()
fig_time = px.line(time_series, title='Daily Threats')
st.plotly_chart(fig_time, use_container_width=True)

# Status of Threat Resolutions
st.subheader("Status of Threat Resolutions")
status_counts = filtered_data['Status'].value_counts().reset_index()
status_counts.columns = ['Status', 'Count']
fig_status = px.pie(status_counts, values='Count', names='Status', title='Threat Resolution Status')
st.plotly_chart(fig_status, use_container_width=True)

# Antivirus Engine Effectiveness
st.subheader("Antivirus Engine Effectiveness")
engine_effectiveness = filtered_data.groupby('Engine')['Status'].value_counts().unstack().fillna(0)
fig_engine = px.bar(engine_effectiveness, barmode='group', title='Engine Effectiveness by Status')
st.plotly_chart(fig_engine, use_container_width=True)

# Display the filtered data table
st.subheader("Filtered Data")
st.dataframe(filtered_data)

# Reset button to clear filters
if st.sidebar.button('Reset Filters'):
    st.experimental_rerun()

# Note on caching
st.info('Data is cached for performance. Adjust filters to view different slices of data.')

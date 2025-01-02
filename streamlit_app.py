import streamlit as st
import pandas as pd
import plotly.express as px

# Cache the data loading for better performance
@st.cache(allow_output_mutation=True)
def load_data():
    url = 'https://raw.githubusercontent.com/dnlaql/Visualize-threat/refs/heads/main/dataset/updated_edr-threat_with_departments.csv'
    data = pd.read_csv(url)
    data['Time Detected'] = pd.to_datetime(data['Time Detected'])
    return data

df = load_data()

# Sidebar for filters
st.sidebar.header('Filters 🎚️')
date_range = st.sidebar.date_input("Date Range 📅", [])
department = st.sidebar.selectbox('Department 🏢', ['All'] + sorted(df['Department'].unique()))
type_filter = st.sidebar.multiselect('Type 🚨', options=sorted(df['Type'].unique()))
status_filter = st.sidebar.multiselect('Status 📊', options=sorted(df['Status'].unique()))
engine_filter = st.sidebar.multiselect('Engine 🖥️', options=sorted(df['Engine'].unique()))

# Filter the data based on user selections
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

# Display the dashboard title and description
st.title('Threat Monitoring and Analysis Dashboard 🛡️')
st.markdown("""
Welcome to the interactive Threat Monitoring Dashboard! This tool is designed to provide insights into network security threats detected over time, enhancing monitoring and decision-making processes.

**Features:**
- Dynamically filter data based on various criteria.
- Interact with visualizations to gain detailed insights.
- Analyze trends and patterns in threat activity.

**Instructions:**
- Use the filters on the left to adjust the data displayed.
- Hover over graphs to see additional details.
""")

# Distribution of Threat Types
fig1 = px.bar(filtered_data, x='Type', title="Distribution of Threat Types")
st.plotly_chart(fig1, use_container_width=True)

# Time Series Analysis of Threat Detection
time_series = filtered_data.groupby(filtered_data['Time Detected'].dt.date).size()
fig2 = px.line(time_series, title='Threats Over Time')
st.plotly_chart(fig2, use_container_width=True)

# Status of Threat Resolutions
status_counts = filtered_data['Status'].value_counts().reset_index()
status_counts.columns = ['Status', 'Count']
fig3 = px.pie(status_counts, values='Count', names='Status', title='Threat Resolution Status')
st.plotly_chart(fig3, use_container_width=True)

# Antivirus Engine Effectiveness
engine_status = filtered_data.groupby(['Engine', 'Status']).size().unstack().fillna(0)
fig4 = px.bar(engine_status, barmode='group', title='Engine Effectiveness by Status')
st.plotly_chart(fig4, use_container_width=True)

# Display filtered data
st.subheader("Filtered Data Table 📝")
st.dataframe(filtered_data)

# Button to reset filters
if st.sidebar.button('Reset Filters 🔄'):
    st.experimental_rerun()

# Footer
st.info('Data is cached for performance. Adjust filters to view different slices of data.')

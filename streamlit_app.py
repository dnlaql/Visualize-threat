import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load your data using Streamlit's new caching method
@st.experimental_memo
def load_data():
    url = 'https://raw.githubusercontent.com/dnlaql/Visualize-threat/refs/heads/main/dataset/updated_edr-threat_with_departments.csv'
    data = pd.read_csv(url)
    data['Time Detected'] = pd.to_datetime(data['Time Detected'])
    return data

df = load_data()

# Initialize session state variables
if 'reset' not in st.session_state:
    st.session_state['reset'] = False

def reset_filters():
    st.session_state['reset'] = True
    st.experimental_rerun()

# Sidebar Filters
st.sidebar.header('Filters')
date_range = st.sidebar.date_input("Date Range", [])
department = st.sidebar.selectbox('Department', ['All'] + list(np.unique(df['Department'])))
threat_type = st.sidebar.multiselect('Type', options=np.unique(df['Type']))
status = st.sidebar.multiselect('Status', options=np.unique(df['Status']))
engine = st.sidebar.multiselect('Engine', options=np.unique(df['Engine']))
if st.sidebar.button('Reset Filters'):
    reset_filters()

# Apply filters
df_filtered = df
if date_range:
    df_filtered = df_filtered[(df_filtered['Time Detected'] >= date_range[0]) & 
                              (df_filtered['Time Detected'] <= date_range[1])]
if department != 'All':
    df_filtered = df_filtered[df_filtered['Department'] == department]
if threat_type:
    df_filtered = df_filtered[df_filtered['Type'].isin(threat_type)]
if status:
    df_filtered = df_filtered[df_filtered['Status'].isin(status)]
if engine:
    df_filtered = df_filtered[df_filtered['Engine'].isin(engine)]

# Dashboard Title
st.title('Threat Analysis Dashboard')

# 1. Distribution of Threat Types (Bar Chart)
st.write("### Distribution of Threat Types")
threat_type_counts = df_filtered['Type'].value_counts()
st.bar_chart(threat_type_counts)

# 2. Time Series Analysis of Threats (Line Chart)
st.write("### Time Series Analysis of Threats")
time_detected = df_filtered.groupby(df_filtered['Time Detected'].dt.date).size()
st.line_chart(time_detected)

# 3. Department Vulnerability Analysis (Bar Chart)
st.write("### Department Vulnerability Analysis")
department_threats = df_filtered['Department'].value_counts()
st.bar_chart(department_threats)

# 4. Status of Threat Resolutions (Pie Chart)
st.write("### Status of Threat Resolutions")
status_counts = df_filtered['Status'].value_counts()
fig, ax = plt.subplots()
ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)

# Display filtered data
st.write("### Filtered Data", df_filtered)

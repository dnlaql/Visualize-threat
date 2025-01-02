import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Using st.cache, which is supported in older and most newer versions
@st.cache
def load_data():
    url = 'https://raw.githubusercontent.com/dnlaql/Visualize-threat/refs/heads/main/dataset/updated_edr-threat_with_departments.csv'
    data = pd.read_csv(url)
    data['Time Detected'] = pd.to_datetime(data['Time Detected'])
    return data

df = load_data()

st.sidebar.header('Filters')
date_range = st.sidebar.date_input("Date Range", [])
department = st.sidebar.selectbox('Department', ['All'] + list(np.unique(df['Department'])))
threat_type = st.sidebar.multiselect('Type', options=np.unique(df['Type']))
status = st.sidebar.multiselect('Status', options=np.unique(df['Status']))
engine = st.sidebar.multiselect('Engine', options=np.unique(df['Engine']))

df_filtered = df
if date_range:
    df_filtered = df_filtered[(df_filtered['Time Detected'] >= date_range[0]) & (df_filtered['Time Detected'] <= date_range[1])]
if department != 'All':
    df_filtered = df_filtered[df_filtered['Department'] == department]
if threat_type:
    df_filtered = df_filtered[df_filtered['Type'].isin(threat_type)]
if status:
    df_filtered = df_filtered[df_filtered['Status'].isin(status)]
if engine:
    df_filtered = df_filtered[df_filtered['Engine'].isin(engine)]

st.title('Threat Analysis Dashboard')
st.write("### Distribution of Threat Types")
threat_type_counts = df_filtered['Type'].value_counts()
st.bar_chart(threat_type_counts)

st.write("### Time Series Analysis of Threats")
time_detected = df_filtered.groupby(df_filtered['Time Detected'].dt.date).size()
st.line_chart(time_detected)

st.write("### Department Vulnerability Analysis")
department_threats = df_filtered['Department'].value_counts()
st.bar_chart(department_threats)

st.write("### Status of Threat Resolutions")
status_counts = df_filtered['Status'].value_counts()
fig, ax = plt.subplots()
ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)

st.write("### Filtered Data", df_filtered)

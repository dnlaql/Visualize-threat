import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load your data using Streamlit's new caching method
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/dnlaql/Visualize-threat/refs/heads/main/dataset/updated_edr-threat_with_departments.csv'
    data = pd.read_csv(url)
    data['Time Detected'] = pd.to_datetime(data['Time Detected'])
    return data

df = load_data()

# Sidebar Filters
st.sidebar.header('Filters')
date_range = st.sidebar.date_input("Date Range", [])
department = st.sidebar.multiselect('Department', options=np.unique(df['Department']))
threat_type = st.sidebar.multiselect('Type', options=np.unique(df['Type']))
status = st.sidebar.multiselect('Status', options=np.unique(df['Status']))
engine = st.sidebar.multiselect('Engine', options=np.unique(df['Engine']))

# Apply filters
df_filtered = df
if date_range:
    df_filtered = df_filtered[(df_filtered['Time Detected'] >= date_range[0]) & 
                              (df_filtered['Time Detected'] <= date_range[1])]
if department:
    df_filtered = df_filtered[df_filtered['Department'].isin(department)]
if threat_type:
    df_filtered = df_filtered[df_filtered['Type'].isin(threat_type)]
if status:
    df_filtered = df_filtered[df_filtered['Status'].isin(status)]
if engine:
    df_filtered = df_filtered[df_filtered['Engine'].isin(engine)]

# Dashboard Title
st.title('Threat Analysis Dashboard')

# Visualization Sections
st.write("### Distribution of Threat Types")
threat_type_counts = df_filtered['Type'].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=threat_type_counts.index, y=threat_type_counts.values, ax=ax)
ax.set_ylabel('Count')
ax.set_xlabel('Threat Type')
st.pyplot(fig)

# Add other visualizations and analyses as needed

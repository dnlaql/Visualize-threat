import streamlit as st
import pandas as pd

# Load your data from a GitHub URL
@st.cache
def load_data():
    url = 'https://raw.githubusercontent.com/dnlaql/Visualize-threat/refs/heads/main/dataset/updated_edr-threat_with_departments.csv'
    data = pd.read_csv(url)
    data['Time Detected'] = pd.to_datetime(data['Time Detected'])
    return data

df = load_data()

# Sidebar for filters
st.sidebar.header('Filters')
date_range = st.sidebar.date_input("Date Range", [])
department_search = st.sidebar.text_input("Search Department")
threat_type = st.sidebar.multiselect('Type', options=df['Type'].unique())
status = st.sidebar.multiselect('Status', options=df['Status'].unique())
engine = st.sidebar.multiselect('Engine', options=df['Engine'].unique())

# Applying filters
df_filtered = df
if date_range:
    df_filtered = df_filtered[(df_filtered['Time Detected'] >= date_range[0]) & (df_filtered['Time Detected'] <= date_range[1])]
if department_search:
    df_filtered = df_filtered[df_filtered['Department'].str.contains(department_search, case=False, na=False)]
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

# 2. Time Series of Threat Detection (Line Chart)
st.write("### Time Series of Threat Detection")
time_detected = df_filtered.groupby(df_filtered['Time Detected'].dt.date).size()
st.line_chart(time_detected)

# 3. Status Distribution (Pie Chart)
st.write("### Status Distribution")
status_counts = df_filtered['Status'].value_counts()
fig, ax = plt.subplots()
ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig)

# 4. Engine Effectiveness (Bar Chart for each Status)
st.write("### Antivirus Engine Effectiveness")
engine_effectiveness = df_filtered.groupby('Engine')['Status'].value_counts().unstack().fillna(0)
st.bar_chart(engine_effectiveness)

# Display filtered data
st.write("### Filtered Data", df_filtered)

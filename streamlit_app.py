import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load your data
@st.cache
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

# 1. Distribution of Threat Types (Bar Chart)
st.write("### Distribution of Threat Types")
threat_type_counts = df_filtered['Type'].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=threat_type_counts.index, y=threat_type_counts.values, ax=ax)
ax.set_ylabel('Count')
ax.set_xlabel('Threat Type')
st.pyplot(fig)

# 2. Time Series Analysis of Threats (Line Chart)
st.write("### Time Series Analysis of Threats")
time_data = df_filtered.groupby(df_filtered['Time Detected'].dt.date).size()
st.line_chart(time_data)

# 3. Department Vulnerability Analysis (Heatmap)
st.write("### Department Vulnerability Analysis")
department_threats = df_filtered.groupby('Department')['Type'].value_counts().unstack().fillna(0)
fig, ax = plt.subplots()
sns.heatmap(department_threats, annot=True, fmt=".0f", linewidths=.5, ax=ax)
st.pyplot(fig)

# 4. Status of Threat Resolutions (Pie Chart)
st.write("### Status of Threat Resolutions")
status_counts = df_filtered['Status'].value_counts()
fig, ax = plt.subplots()
ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig)

# 5. Effectiveness of Antivirus Engines (Stacked Bar Chart)
st.write("### Effectiveness of Antivirus Engines")
engine_status = df_filtered.groupby(['Engine', 'Status']).size().unstack().fillna(0)
engine_status.plot(kind='bar', stacked=True)
st.pyplot(plt)

# 6. Correlation Analysis (Correlation Heatmap)
st.write("### Correlation Analysis")
# Example: Assume there are numerical columns to correlate
if 'Severity' in df.columns and 'Response Time' in df.columns:  # Example numerical columns
    correlation_matrix = df_filtered[['Severity', 'Response Time']].corr()
    fig, ax = plt.subplots()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

# 7. Threat Source Analysis (Geographical Map) - Example Placeholder
st.write("### Threat Source Analysis")
st.write("This would typically display a geographical map based on IP geolocation data.")

# Display filtered data
st.write("### Filtered Data", df_filtered)

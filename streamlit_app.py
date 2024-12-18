import streamlit as st
import pandas as pd
import datetime as dt

# Mapping of IP segments to departments
IP_MAPPING = {
    "172.22.58": "NICU DEPARTMENT",
    "172.22.59": "IT DEPARTMENT",
    "172.22.60": "FINANCE DEPARTMENT",
    # Add other mappings as needed
}

# Function to map IP addresses to departments
def map_ip_to_department(ip_address):
    segment = ".".join(ip_address.split(".")[:3])  # Extract the first three octets
    return IP_MAPPING.get(segment, "Unknown Department")

# Sample Data (Replace with your dataset)
data = {
    "No.": [1, 2, 3],
    "Time Detected": ["29/11/2024 15:38", "29/11/2024 16:00", "30/11/2024 10:15"],
    "Endpoint": ["2F-PC-205", "2F-PC-206", "2F-PC-207"],
    "IP Address": ["172.22.58.194", "172.22.59.105", "172.22.60.200"],
    "Type": ["Trojan", "Malware", "Trojan"],
    "Threat": ["Trojan.Win64.Agent.A7eg", "Malware.Generic", "Trojan.Win32.Cryptor"],
    "Infected File": [
        "c:\\programdata\\bkyzejjgqxyc.exe",
        "c:\\windows\\system32\\malicious.dll",
        "c:\\users\\admin\\cryptor.exe",
    ],
    "Time Created": ["10/02/2024 8:41", "12/02/2024 9:20", "15/02/2024 10:00"],
    "File MD5": [
        "C112A7B5E5320C16AC6D5BF2D3B63D53",
        "A211B7F5C4321C18DC6D5BF2D4C64E32",
        "B123C8A7D6322C20FC6E5BF3E5B65F43",
    ],
    "Status": ["Isolated successfully.", "Pending", "Isolated successfully."],
    "Time Fixed": ["29/11/2024 15:39", None, "30/11/2024 10:20"],
    "Engine": [
        "Sangfor Cloud-Based Antivirus Engine",
        "Avast Antivirus Engine",
        "McAfee Antivirus Engine",
    ],
    "Antivirus database version": ["2.024110e+13", "2.024111e+13", "2.024112e+13"],
}

# Convert data to DataFrame
df = pd.DataFrame(data)

# Add Department column
df["Department"] = df["IP Address"].apply(map_ip_to_department)

# Convert time columns to datetime
df["Time Detected"] = pd.to_datetime(df["Time Detected"], format="%d/%m/%Y %H:%M")
df["Time Created"] = pd.to_datetime(df["Time Created"], format="%d/%m/%Y %H:%M")
if "Time Fixed" in df.columns:
    df["Time Fixed"] = pd.to_datetime(df["Time Fixed"], errors="coerce")

# App title
st.title("First-Level Threat Analysis Dashboard")

# Sidebar Filters
st.sidebar.header("Filter Options")
departments = st.sidebar.multiselect("Select Departments", df["Department"].unique(), default=df["Department"].unique())
statuses = st.sidebar.multiselect("Select Threat Status", df["Status"].unique(), default=df["Status"].unique())

# Apply filters
filtered_df = df[(df["Department"].isin(departments)) & (df["Status"].isin(statuses))]

# Display filtered data
st.subheader("Threat Data")
st.dataframe(filtered_df)

# Summary Insights
st.subheader("Summary Insights")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Threats", len(filtered_df))
with col2:
    isolated_count = len(filtered_df[filtered_df["Status"] == "Isolated successfully."])
    st.metric("Isolated Threats", isolated_count)
with col3:
    pending_count = len(filtered_df[filtered_df["Status"] == "Pending"])
    st.metric("Pending Threats", pending_count)

# Visualization: Threats by Department
st.subheader("Threats by Department")
department_counts = filtered_df["Department"].value_counts()
st.bar_chart(department_counts)

# Visualization: Threat Types
st.subheader("Threat Types")
type_counts = filtered_df["Type"].value_counts()
st.bar_chart(type_counts)

# Timeline of Threats
st.subheader("Threat Detection Over Time")
threats_over_time = filtered_df.groupby(filtered_df["Time Detected"].dt.date).size()
st.line_chart(threats_over_time)

# Alert for High-Risk Departments
if not department_counts.empty:
    high_risk_department = department_counts.idxmax()
    st.warning(f"⚠️ High threat activity detected in {high_risk_department}!")

# Download Filtered Data
st.subheader("Download Filtered Data")
@st.cache
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

csv_data = convert_df_to_csv(filtered_df)
st.download_button(
    label="Download Report as CSV",
    data=csv_data,
    file_name="threat_analysis_report.csv",
    mime="text/csv",
)

st.success("Dashboard Loaded Successfully!")

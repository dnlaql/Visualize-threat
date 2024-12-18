import streamlit as st
import pandas as pd

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

# App title
st.title("First-Level Threat Analysis Dashboard")

# GitHub dataset URL
DATA_URL = "https://raw.githubusercontent.com/dnlaql/Visualize-threat/refs/heads/main/dataset/threat.csv"

# Load the dataset
@st.cache_data
def load_data(url):
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()  # Remove leading/trailing spaces from column names
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data(DATA_URL)

if not df.empty:
    # Add Department column based on IP Address
    if "IP Address" in df.columns:
        df["Department"] = df["IP Address"].apply(map_ip_to_department)
    else:
        st.error("The dataset does not contain the required 'IP Address' column.")
        st.stop()

    # Convert time columns to datetime if available
    if "Time Detected" in df.columns:
        df["Time Detected"] = pd.to_datetime(df["Time Detected"], errors="coerce")
    if "Time Created" in df.columns:
        df["Time Created"] = pd.to_datetime(df["Time Created"], errors="coerce")
    if "Time Fixed" in df.columns:
        df["Time Fixed"] = pd.to_datetime(df["Time Fixed"], errors="coerce")

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
    if "Time Detected" in df.columns:
        threats_over_time = filtered_df.groupby(filtered_df["Time Detected"].dt.date).size()
        st.line_chart(threats_over_time)

    # Alert for High-Risk Departments
    if not department_counts.empty:
        high_risk_department = department_counts.idxmax()
        st.warning(f"⚠️ High threat activity detected in {high_risk_department}!")

    # Download Filtered Data
    st.subheader("Download Filtered Data")
    @st.cache_data
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
else:
    st.info("Dataset is empty or could not be loaded.")

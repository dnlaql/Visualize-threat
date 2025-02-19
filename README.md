# Threat Monitoring and Analysis Dashboard

## Overview
The **Threat Monitoring and Analysis Dashboard** is an interactive tool designed to help organizations monitor, analyze, and respond to cybersecurity threats. Built with **Streamlit**, this dashboard provides real-time insights into detected threats, their distribution across departments, trends over time, and the effectiveness of antivirus engines.

## Features

### 🔍 Interactive Filters
Users can dynamically filter data using multiple criteria:

- **Date Range 📅**: View threats detected within a specific time frame.
- **Department 🏢**: Analyze threats based on organizational departments.
- **Type 🚨**: Select specific threat types for analysis.
- **Status 📊**: Review the resolution status of detected threats.
- **Engine 🖥️**: Assess the performance of different antivirus engines.
- **Reset Filters 🔄**: Easily reset all filters to default settings.

### 📊 Data Visualizations
- **Threat Distribution by Department**: A bar chart illustrating which departments experience the most security threats.
- **Time Series Analysis**: A line chart tracking the daily volume of detected threats.
- **Threat Resolution Status**: A pie chart breaking down the status of threat resolutions.
- **Antivirus Engine Effectiveness**: A grouped bar chart comparing antivirus performance based on resolved threats.
- **Filtered Data Table**: A dynamic table displaying the filtered dataset.

## Technology Stack
- **Python 🐍**: Core programming language.
- **Streamlit 🎨**: Web framework for dashboarding.
- **Pandas 📊**: Data processing and analysis.
- **Plotly 📈**: Interactive visualization library.

## Data Source
The dashboard loads and processes data from the following dataset:

- **URL**: [Threat Dataset](https://raw.githubusercontent.com/dnlaql/Visualize-threat/refs/heads/main/dataset/updated_edr-threat_with_departments.csv)
- **Dataset Features**:
  - `Time Detected`: Timestamp of threat detection.
  - `Department`: Organizational unit affected.
  - `Type`: Category of the detected threat.
  - `Status`: Resolution status (e.g., Resolved, Pending, Active).
  - `Engine`: Antivirus engine used for detection.

## Objective
The primary goal of this dashboard is to **enhance cybersecurity monitoring and response** by:
- Providing a **centralized** and **visual representation** of security threats.
- Allowing security teams to **identify trends and vulnerabilities** within the organization.
- Helping decision-makers **evaluate the performance of different security tools**.

## How to Use
1. **Run the Dashboard**:
   ```bash
   streamlit run app.py

## Go to Dashboard Link
**URL**: https://threatmonitoring-mini.streamlit.app/

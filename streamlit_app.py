import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Dataset URL
DATA_URL = "https://raw.githubusercontent.com/dnlaql/Visualize-threat/refs/heads/main/dataset/threat%20(1).csv"

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

# Check if the dataset is loaded
if df.empty:
    st.error("The dataset could not be loaded.")
else:
    st.write("Dataset Overview")
    st.write(df.head())  # Show first few rows
    
    # Data Types and Missing Values
    st.write("Data Types and Missing Values")
    st.write(df.info())
    st.write("Missing Values per Column")
    st.write(df.isnull().sum())
    
    # Descriptive Statistics
    st.write("Descriptive Statistics")
    st.write(df.describe())
    
    # Column-wise distribution of categorical variables
    st.write("Threat Type Distribution")
    st.bar_chart(df['Type'].value_counts())
    
    # Time analysis
    st.write("Threat Detection Over Time")
    df['Time Detected'] = pd.to_datetime(df['Time Detected'], errors='coerce')
    time_detected = df.groupby(df['Time Detected'].dt.date).size()
    st.line_chart(time_detected)
    
    # Bar chart for status
    st.write("Threat Status Distribution")
    st.bar_chart(df['Status'].value_counts())
    
    # Visualize correlations using a heatmap (for numerical columns)
    st.write("Correlation Heatmap")
    corr_matrix = df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    st.pyplot()

    # Box plot for numerical features to check for outliers
    st.write("Boxplot for Numerical Features")
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numerical_cols:
        plt.figure(figsize=(8, 6))
        sns.boxplot(x=df[col])
        st.pyplot()
    
    st.success("EDA completed successfully!")

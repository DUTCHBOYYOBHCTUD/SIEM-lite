import streamlit as st
import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect('database/siem.db')
cursor = conn.cursor()

# Load alerts into DataFrame
def load_alerts():
    query = "SELECT timestamp, ip_address, alert_type, severity, description FROM alerts ORDER BY timestamp DESC"
    return pd.read_sql_query(query, conn)

# Streamlit App
st.set_page_config(page_title="SIEM-lite Dashboard", layout="wide")
st.title("🔐 SIEM-lite - Alerts Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")
severity_filter = st.sidebar.multiselect("Select Severity", ["High", "Medium", "Low"], default=["High", "Medium", "Low"])
ip_filter = st.sidebar.text_input("Search by IP address")

# Load and filter data
alerts_df = load_alerts()
if severity_filter:
    alerts_df = alerts_df[alerts_df["severity"].isin(severity_filter)]
if ip_filter:
    alerts_df = alerts_df[alerts_df["ip_address"].str.contains(ip_filter)]

# Display
st.dataframe(alerts_df, use_container_width=True)

# Summary Stats
st.markdown("### 📊 Summary")
col1, col2 = st.columns(2)
col1.metric("Total Alerts", len(alerts_df))
col2.metric("Unique IPs", alerts_df["ip_address"].nunique())

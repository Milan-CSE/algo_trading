import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(layout="wide", page_title="Company Returns Visualizer")
st.title("📊 Company Returns Over 2 Years")

# Load the returns data
try:
    df = pd.read_csv("investment_summary.csv")
except FileNotFoundError:
    st.error("❌ File 'investment_summary.csv' not found.")
    st.stop()

# Rename for consistency (optional, avoids special characters)
df.rename(columns={"Return %": "Return_Percent"}, inplace=True)

# Sort by return
df = df.sort_values(by="Return_Percent", ascending=False)

# Bar chart of returns
fig = px.bar(
    df,
    x='Company',
    y='Return_Percent',
    title='2-Year Return Comparison by Company',
    color='Return_Percent',
    color_continuous_scale='Viridis',
    labels={'Return_Percent': 'Return (%)'},
)

fig.update_layout(
    xaxis_tickangle=-45,
    height=600,
    margin=dict(l=40, r=40, t=80, b=40)
)

# Display chart and data
st.plotly_chart(fig, use_container_width=True)
st.subheader("📋 Return Data Table")
st.dataframe(df.reset_index(drop=True), use_container_width=True)

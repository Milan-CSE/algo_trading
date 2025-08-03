import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from plotly.subplots import make_subplots


st.set_page_config(layout="wide")
st.title("📈 Company Stock Candlestick + RSI Chart")

DATA_DIR = "data/"

# 🔽 Dropdown to pick company
files = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
company_file = st.selectbox("Select a company:", files)
file_path = os.path.join(DATA_DIR, company_file)

# 📥 Load data
df = pd.read_csv(file_path)
df.columns = df.columns.str.lower()

# 🧹 Clean and prepare
df['timestamp'] = pd.to_datetime(df['timestamp'], dayfirst=True)
df = df.sort_values("timestamp")

# 📊 Candlestick chart
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                    vertical_spacing=0.05,
                    row_heights=[0.7, 0.3],
                    subplot_titles=("Candlestick Chart", "RSI"))

fig.add_trace(go.Candlestick(
    x=df['timestamp'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close'],
    name='OHLC'
), row=1, col=1)

# 📉 RSI line
fig.add_trace(go.Scatter(
    x=df['timestamp'],
    y=df['rsi'],
    line=dict(color='blue', width=1),
    name="RSI"
), row=2, col=1)

# 🛠️ RSI threshold lines
fig.add_hline(y=70, line=dict(color='red', dash='dash'), row=2, col=1)
fig.add_hline(y=30, line=dict(color='green', dash='dash'), row=2, col=1)

fig.update_layout(height=700, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

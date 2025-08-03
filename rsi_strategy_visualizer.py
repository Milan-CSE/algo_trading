import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from pathlib import Path

# RSI calculation
def compute_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Buy/Sell/Stable signal function
def generate_signals(df):
    df['Signal'] = 'Stable'
    df.loc[df['RSI'] < 30, 'Signal'] = 'Buy'
    df.loc[df['RSI'] > 70, 'Signal'] = 'Sell'
    return df

# Streamlit UI
st.set_page_config(layout="wide")
st.title("📉 RSI Strategy Candlestick Visualizer")

# File selector
data_path = Path("data")
files = list(data_path.glob("*.csv"))
file_names = [f.name for f in files]
selected_file = st.selectbox("Select company CSV", file_names)

# Load selected CSV
df = pd.read_csv(data_path / selected_file)

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Calculate RSI
df['RSI'] = compute_rsi(df)
df = generate_signals(df)

# Candlestick chart
fig_candle = go.Figure(data=[
    go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Price'
    )
])

# Add Buy/Sell markers
buy_signals = df[df['Signal'] == 'Buy']
sell_signals = df[df['Signal'] == 'Sell']

fig_candle.add_trace(go.Scatter(
    x=buy_signals.index,
    y=buy_signals['Close'],
    mode='markers',
    marker=dict(color='green', size=8),
    name='Buy Signal'
))

fig_candle.add_trace(go.Scatter(
    x=sell_signals.index,
    y=sell_signals['Close'],
    mode='markers',
    marker=dict(color='red', size=8),
    name='Sell Signal'
))

fig_candle.update_layout(title="Candlestick Chart with Buy/Sell Signals")

# RSI chart
fig_rsi = go.Figure()
fig_rsi.add_trace(go.Scatter(
    x=df.index, y=df['RSI'],
    mode='lines',
    name='RSI',
    line=dict(color='orange')
))
fig_rsi.add_hline(y=30, line=dict(dash='dash', color='green'))
fig_rsi.add_hline(y=70, line=dict(dash='dash', color='red'))
fig_rsi.add_hline(y=50, line=dict(dash='dot', color='gray'))
fig_rsi.update_layout(title="RSI Chart")

# Show charts
st.plotly_chart(fig_candle, use_container_width=True)
st.plotly_chart(fig_rsi, use_container_width=True)

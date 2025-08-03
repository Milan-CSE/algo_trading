import streamlit as st
import os
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Candlestick + RSI Viewer", layout="wide")
st.title("📊 Candlestick & RSI Chart Viewer for 50 Companies")

DATA_FOLDER = "data"

# Get CSV files
csv_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]
selected_file = st.selectbox("Select Company", sorted(csv_files))

if selected_file:
    filepath = os.path.join(DATA_FOLDER, selected_file)
    df = pd.read_csv(filepath)

    required_cols = {'timestamp', 'open', 'high', 'low', 'close', 'RSI'}
    if not required_cols.issubset(df.columns):
        st.error(f"File '{selected_file}' is missing one of the required columns: {required_cols}")
    else:
        # Convert timestamp
        df['Date'] = pd.to_datetime(df['timestamp'], format='%d-%m-%Y %H:%M', errors='coerce')

        # Main Candlestick Chart
        fig_candle = go.Figure()
        fig_candle.add_trace(go.Candlestick(
            x=df['Date'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Candles'
        ))
        fig_candle.update_layout(
            title=f"{selected_file.replace('.csv', '')} - Candlestick Chart",
            xaxis_title="Date",
            yaxis_title="Price",
            xaxis_rangeslider_visible=False,
            height=600,
        )
        st.plotly_chart(fig_candle, use_container_width=True)

        # RSI Line Chart
        fig_rsi = go.Figure()
        fig_rsi.add_trace(go.Scatter(
            x=df['Date'],
            y=df['RSI'],
            mode='lines',
            name='RSI',
            line=dict(color='orange')
        ))
        fig_rsi.add_hline(y=70, line=dict(dash='dash', color='red'))
        fig_rsi.add_hline(y=30, line=dict(dash='dash', color='green'))

        fig_rsi.update_layout(
            title="Relative Strength Index (RSI)",
            xaxis_title="Date",
            yaxis_title="RSI Value",
            height=300,
            yaxis=dict(range=[0, 100])
        )

        st.plotly_chart(fig_rsi, use_container_width=True)

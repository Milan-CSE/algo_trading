import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components
import time

st.set_page_config(layout="wide")

st.markdown("<style>body {scroll-behavior: smooth;}</style>", unsafe_allow_html=True)
st.title("📈 Live BTC Algo Trading Bot")

refresh_interval = 5

# Track last refresh in session
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()

# Refresh timer display
elapsed = time.time() - st.session_state.last_update
countdown = int(refresh_interval - elapsed)

col1, col2 = st.columns([1, 5])
with col1:
    if countdown <= 0:
        st.session_state.last_update = time.time()
        
    else:
        st.button(f"🔄 Refreshing in {countdown}s", disabled=True)
# 🔄 Auto-refresh every 5 seconds
#st_autorefresh(interval=5000, key="refresh-timer")

# CSV file where ws_streamer or live_strategy_runner writes latest data
DATA_PATH = Path("data/live_data.csv")

# Sidebar options
timeframe = st.selectbox("Timeframe", options=["1m", "5m", "15m"], index=1)
show_ma5 = st.checkbox("Show 5 MA", value=True)
show_ma20 = st.checkbox("Show 20 MA", value=True)



chart_placeholder = st.empty()


# 📊 Load and plot live data
if DATA_PATH.exists():
    try:
        df = pd.read_csv(DATA_PATH)

        if len(df) < 2:
            empty_fig = go.Figure()
            empty_fig.update_layout(height=600, template='plotly_dark')
            chart_placeholder.plotly_chart(empty_fig, use_container_width=True)
            st.warning("Waiting for more live candles...")

        else:
            fig = go.Figure()

            fig.add_trace(go.Candlestick(
                x=df['timestamp'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name='BTC/USD',
                increasing_line_color='lime', 
                decreasing_line_color='red',
                showlegend=False,
                
            ))


        # === Overlay 5 MA ===
        if show_ma5 and '5_MA' in df.columns:
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['5_MA'],
                mode='lines',
                name='5 MA',
                line=dict(width=1.8, color='cyan')
            ))

        # === Overlay 20 MA ===
        if show_ma20 and '20_MA' in df.columns:
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['20_MA'],
                mode='lines',
                name='20 MA',
                line=dict(width=1.8, color='orange')
            ))

        # === Buy / Sell signals ===
        buy_signals = df[df['Signal'] == 'BUY']
        sell_signals = df[df['Signal'] == 'SELL']

        fig.add_trace(go.Scatter(
            x=buy_signals['timestamp'],
            y=buy_signals['low'],
            mode='markers',
            name='BUY',
            marker=dict(symbol='triangle-up', size=12, color='lime'),
            showlegend=True
        ))

        fig.add_trace(go.Scatter(
            x=sell_signals['timestamp'],
            y=sell_signals['high'],
            mode='markers',
            name='SELL',
            marker=dict(symbol='triangle-down', size=12, color='red'),
            showlegend=True
        ))

        # === Upgrade layout to TradingView style ===
        fig.update_layout(
            template='plotly_dark',
            xaxis_rangeslider_visible=False,
            height=600,
            plot_bgcolor='#0f0f0f',
            paper_bgcolor='#0f0f0f',
            xaxis=dict(
                showgrid=True,
                gridcolor='#2e2e2e',
                tickangle=-45,
                tickfont=dict(color='white'),
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#2e2e2e',
                tickfont=dict(color='white'),
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=12, color='white')
            ),
            margin=dict(l=10, r=10, t=40, b=10)
        )
        # Ensure only chart is refresh not the whole app
        # Ensure only chart is refresh not the whole app
        with chart_placeholder:
            st.plotly_chart(fig, use_container_width=True, config={
                "scrollZoom": True,
                "displayModeBar": True,
                "responsive": True,
                "doubleClick": "reset",  # 🔧 Reset on double click
                "modeBarButtonsToAdd": ["zoom2d", "pan2d", "resetScale2d", "autoScale2d"],
            })


    except Exception as e:
        st.error(f"Error loading data: {e}")
else:
    st.warning("Waiting for data file to be created...")

# 📺 TradingView live widget
st.subheader("📺 TradingView Live BTC Chart")

components.html("""
<!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
  <div id="tradingview_btc"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget({
    "width": "100%",
    "height": 600,
    "symbol": "BINANCE:BTCUSDT",
    "interval": "5",
    "timezone": "Etc/UTC",
    "theme": "dark",
    "style": "1",
    "locale": "en",
    "toolbar_bg": "#f1f3f6",
    "enable_publishing": false,
    "allow_symbol_change": true,
    "container_id": "tradingview_btc"
  });
  </script>
</div>
<!-- TradingView Widget END -->
""", height=600)

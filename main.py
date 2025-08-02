import pandas as pd
from src.strategy import moving_average_crossover_strategy
from src.simulator import simulate_trading
from src.plots import plot_signals

#  Load your historical stock data
df = pd.read_csv("data/nestle.csv")

def compute_rsi(df, window):
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

df["5_MA"] = df["Close"].rolling(5).mean()
df["20_MA"] = df["Close"].rolling(20).mean()
df["50_MA"] = df["Close"].rolling(50).mean()
df["RSI_14"] = compute_rsi(df, 14)


#  Generate Buy/Sell Signals
df = moving_average_crossover_strategy(df)

#  Simulate trading
trade_log, final_balance = simulate_trading(df)

# Show results
print("\n--- TRADE LOG ---")
for entry in trade_log:
    print(entry)

print(f"\n Final Balance: ₹{final_balance:.2f}")

# Plot results
plot_signals(df)
print(df["Signal"].value_counts())



#  Calculate win rate
def calculate_win_rate(trade_log):
    wins = 0
    total = 0

    buy_price = None

    for entry in trade_log:
        if "BUY at" in entry:
            try:
                buy_price = float(entry.split("BUY at")[1].split(",")[0].strip())
            except:
                buy_price = None

        elif "SELL at" in entry or "FINAL SELL at" in entry:
            try:
                sell_price = float(entry.split("at")[1].split(",")[0].strip())
                if buy_price is not None:
                    total += 1
                    if sell_price > buy_price:
                        wins += 1
                    buy_price = None  # reset for next trade
            except:
                continue

    win_rate = (wins / total) * 100 if total > 0 else 0
    return round(win_rate, 2), total




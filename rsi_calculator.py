import os
import pandas as pd

def calculate_rsi(data: pd.DataFrame, period: int = 14) -> pd.Series:
    delta = data['close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

# --- Main Code ---
DATA_DIR = "data/"

for filename in os.listdir(DATA_DIR):
    if filename.endswith(".csv"):
        filepath = os.path.join(DATA_DIR, filename)
        df = pd.read_csv(filepath)

        # Standardize columns
        df.columns = df.columns.str.lower()

        # Required columns for RSI
        required_cols = {'timestamp', 'close'}
        if not required_cols.issubset(set(df.columns)):
            print(f"[❌] File '{filename}' is missing required columns: {required_cols - set(df.columns)}")
            continue

        df['rsi'] = calculate_rsi(df)

        df.to_csv(filepath, index=False)
        print(f"[✅] RSI added to {filename}")

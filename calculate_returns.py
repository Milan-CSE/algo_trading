import pandas as pd
from pathlib import Path

# Set path to your local data folder (change if needed)
data_folder = Path("data")

# Define column headers
columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']

# Starting capital per company
initial_investment = 100000

# Store results here
results = []

# Loop through all CSV files in the folder
for file in data_folder.glob("*.csv"):
    try:
        # Read CSV with no header
        df = pd.read_csv(file, header=None, names=columns)

        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp'])

        # Sort by date just in case
        df = df.sort_values('timestamp')

        # Use first and last close prices
        start_price = df.iloc[0]['close']
        end_price = df.iloc[-1]['close']

        shares = initial_investment / start_price
        final_value = shares * end_price
        return_percent = ((final_value - initial_investment) / initial_investment) * 100

        results.append({
            "Company": file.stem,
            "Start Price": round(start_price, 2),
            "End Price": round(end_price, 2),
            "Final Value": round(final_value, 2),
            "Return %": round(return_percent, 2)
        })

    except Exception as e:
        print(f"Error processing {file.name}: {e}")

# Convert results to DataFrame and sort
summary_df = pd.DataFrame(results).sort_values(by="Return %", ascending=False)
summary_df.reset_index(drop=True, inplace=True)

# Show results
print(summary_df)

# Optionally save to CSV
summary_df.to_csv("investment_summary.csv", index=False)

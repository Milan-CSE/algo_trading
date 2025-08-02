def simulate_trading(df):
    initial_balance = 10000
    balance = initial_balance
    position = 0
    entry_price = 0

    trade_log = []
    win_count = 0
    total_trades = 0

    for i in range(len(df)):
        signal = df["Signal"].iloc[i]
        date = df["Date"].iloc[i] if "Date" in df.columns else i
        price = df["Low"].iloc[i]

        if signal == "BUY" and position == 0:
            position = balance // price
            entry_price = price
            balance -= position * price
            trade_log.append(f"{date}: BUY at {price:.2f}, Balance: {balance:.2f}, Position: {position}")


        elif signal == "SELL" and position > 0:
            balance += position * price
            gain_loss_pct = ((price - entry_price) / entry_price) * 100
            trade_log.append(f"{date}: SELL at {price:.2f}, Gain/Loss: {gain_loss_pct:.2f}%, Balance: {balance:.2f}, Position: 0")

            if price > entry_price:
                win_count += 1
            total_trades += 1

            position = 0
            entry_price = 0
       
    # Final value if still holding
    if position > 0:
        final_price = df["Low"].iloc[-1]
        date = df["Date"].iloc[-1] if "Date" in df.columns else "END"
        balance += position * final_price
        gain_loss_pct = ((final_price - entry_price) / entry_price) * 100
        trade_log.append(f"{date}: FINAL SELL at {final_price:.2f}, Gain/Loss: {gain_loss_pct:.2f}%, Balance: {balance:.2f}, Position: 0")

        if final_price > entry_price:
            win_count += 1
        total_trades += 1

    win_rate = (win_count / total_trades) * 100 if total_trades > 0 else 0
    print(f"Final Balance: ₹{balance:.2f}")
    print(f"Total Trades: {total_trades}")
    print(f"Winning Trades: {win_count}")
    print(f"Win Rate: {win_rate:.2f}%")

    return trade_log, balance

def moving_average_crossover_strategy(df):
    """
    This strategy generates BUY/SELL/HOLD signals using a moving average crossover.
    """

    signals = []
    holding = False
    entry_price = 0
    peak_price = 0

    take_profit_percent = 0.05  # 5% trailing stop-loss

    # Looping through each row (starting from index 1)
    for i in range(1, len(df)):
        sma_long_today = df['20_MA'].iloc[i]
        sma_short_today = df['5_MA'].iloc[i]

        sma_long_prev = df['20_MA'].iloc[i - 1]
        sma_short_prev = df['5_MA'].iloc[i - 1]

        #rsi_today = df['RSI_14'].iloc[i]
        price = df['Low'].iloc[i]

        # BUY signal: short MA crosses above long MA + oversold(RSI < 30)
        if sma_short_prev < sma_long_prev and sma_short_today > sma_long_today and not holding:
            print(f"BUY SIGNAL on {df['Date'].iloc[i]}")
            signals.append("BUY")
            holding = True
            entry_price = price
            peak_price = price
            continue
           

        # SELL signal: short MA crosses below long MA
        if holding:

            # Update peak price if current price is the highest so far
            if price > peak_price:
                peak_price = price

            # Hard stop-loss: Sell if price drops 5% from entry
            if price < entry_price * 0.95:
                print(f"[HARD STOP] {df['Date'].iloc[i]} - Entry: {entry_price:.2f}, Price: {price:.2f}")
                signals.append("SELL")
                holding = False
                continue

            # Take profit: Sell if price increases by 5% from entry
            if price >= entry_price * (1 + take_profit_percent):
                signals.append("SELL")
                holding = False
                continue
            
            # Trailing stop-loss: Sell if price drops 5% from peak
            if price < peak_price * 0.95:
                signals.append("SELL")
                holding = False
                continue
            
            if sma_short_prev > sma_long_prev and sma_short_today < sma_long_today :
                signals.append("SELL")
                holding = False
                continue
            
            signals.append("HOLD")
            continue
                

        # HOLD if no crossover
        
        signals.append("HOLD")

    # First row has no signal because there's no previous row
    signals.insert(0, "HOLD")

    # Add signals to the DataFrame
    df["Signal"] = signals

    # Return the updated DataFrame with signals
    return df

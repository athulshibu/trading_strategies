import numpy as np
import pandas as pd

def calculate_breakout_pullback(df, breakout_period, pullback_threshold):
    df['HighThreshold'] = df['high'].rolling(window=breakout_period).max()
    df['LowThreshold'] = df['low'].rolling(window=breakout_period).min()
    df['Breakout'] = np.where(df['price'] > df['HighThreshold'], 1, np.where(df['price'] < df['LowThreshold'], -1, 0))
    
    df['PullbackHigh'] = df['HighThreshold'] * (1 - pullback_threshold)
    df['PullbackLow'] = df['LowThreshold'] * (1 + pullback_threshold)
    
    return df

def breakout_pullback_strategy(df, breakout_period, pullback_threshold, holding_period):
    df = calculate_breakout_pullback(df, breakout_period, pullback_threshold)
    df['position'] = 0
    df['signal'] = 0
    
    for i in range(len(df)):
        if df['Breakout'].iloc[i] == 1 and df['price'].iloc[i] > df['PullbackHigh'].iloc[i-1]:
            df.at[df.index[i], 'position'] = 1
        elif df['Breakout'].iloc[i] == -1 and df['price'].iloc[i] < df['PullbackLow'].iloc[i-1]:
            df.at[df.index[i], 'position'] = -1
            
        if df['position'].iloc[i] == 1 and df['position'].iloc[i-1] == 0:
            df.at[df.index[i], 'signal'] = 1
        elif df['position'].iloc[i] == -1 and df['position'].iloc[i-1] == 0:
            df.at[df.index[i], 'signal'] = -1
    
    df['position'] = df['position'].ffill().fillna(0)
    df['signal'] = df['signal'].ffill().fillna(0)

    # Simulate trading and calculate returns
    df['Return'] = df['signal'].shift(-holding_period) * (df['price'].pct_change())
    return df

# Assuming you have a DataFrame 'data' containing 'Timestamp', 'high', 'low', and 'price' columns
price_data = pd.read_csv('btc_price_data.csv')
breakout_period = 20
pullback_threshold = 0.1
holding_period = 5

result = breakout_pullback_strategy(price_data, breakout_period, pullback_threshold, holding_period)
print(result)
result.to_csv('btc_signals.csv', index=False)
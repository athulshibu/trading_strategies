import numpy as np
import pandas as pd

def calculate_bollinger_bands(df, window, num_std):
    rolling_mean = df['price'].rolling(window=window).mean()
    rolling_std = df['price'].rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    return upper_band, lower_band

def mean_reversion_strategy(df, window, num_std, zscore_threshold, holding_period):
    # df['upperBand'], df['lowerBand'] = calculate_bollinger_bands(df, window, num_std)
    df['ZScore'] = (df['price'] - df['price'].rolling(window=window).mean()) / df['price'].rolling(window=window).std()
    
    df['position'] = 0
    df['signal'] = 0
    
    for i in range(len(df)):
        if df['ZScore'].iloc[i] < -zscore_threshold:
            df.at[df.index[i], 'position'] = 1
        elif df['ZScore'].iloc[i] > zscore_threshold:
            df.at[df.index[i], 'position'] = -1
            
        if df['position'].iloc[i] == 1 and df['position'].iloc[i-1] == 0:
            df.at[df.index[i], 'signal'] = 1
        elif df['position'].iloc[i] == -1 and df['position'].iloc[i-1] == 0:
            df.at[df.index[i], 'signal'] = -1
    
    df['position'] = df['position'].ffill().fillna(0)
    df['signal'] = df['signal'].ffill().fillna(0)
    
    df['Return'] = df['signal'].shift(-holding_period) * (df['price'].pct_change())
    return df


price_data = pd.read_csv('btc_price_data.csv')  # CSV file should have 'Timestamp' and 'price'
window = 5 # for calculating rolling mean
num_std = 1 # num_std controls the Bollinger bands. Lower the band, higher the risk
zscore_threshold = 0.4 # Threshold to generate trades. lower the z-score, more the number of trades, consequently, more the risk
holding_period = 10 # time (in minutes because of the dataset) of holding onto trades

result = mean_reversion_strategy(price_data, window, num_std, zscore_threshold, holding_period)
print(result)
result.to_csv('btc_signals.csv', index=False)
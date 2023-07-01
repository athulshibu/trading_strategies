import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller

def pair_trading_strategy(data, asset1, asset2, entry_threshold, exit_threshold):
    data['position'] = 0
    data.loc[data['z_score'] > entry_threshold, 'position'] = -1
    data.loc[data['z_score'] < -entry_threshold, 'position'] = 1
    data.loc[abs(data['z_score']) < exit_threshold, 'position'] = 0

    data['signal'] = data['position'].diff()
    data['position'] = data['position'].ffill().fillna(0)
    data['signal'] = data['signal'].ffill().fillna(0)

    return data

asset1_data = pd.read_csv('btc_price_data.csv')
asset2_data = pd.read_csv('eth_price_data.csv')

merged_data = pd.merge(asset1_data, asset2_data, on='Timestamp', suffixes=('_asset1', '_asset2'))

merged_data['spread'] = merged_data['price_asset1'] - merged_data['price_asset2']
adfuller = adfuller(merged_data['spread'])
test_statistic = adfuller[0]
p_value = adfuller[1]
critical_values = adfuller[4]

significance_level = 0.05
critical_value_5percent = critical_values['5%']

print("ADF Test Statistic:", test_statistic)
print("p-value:", p_value)
print("Critical Value (5%):", critical_value_5percent)

# Interpret the ADF test result
if test_statistic < critical_value_5percent:
    print("The spread is stationary. Proceed with pairs trading strategy.")
else:
    print("The spread is non-stationary. Pairs trading may not be suitable.")


spread_mean = merged_data['spread'].mean()
spread_std = merged_data['spread'].std()
merged_data['z_score'] = (merged_data['spread'] - spread_mean) / spread_std
entry_threshold = 0.7
exit_threshold = 0.5

result = pair_trading_strategy(merged_data, 'price_asset1', 'price_asset2', entry_threshold, exit_threshold)
result.rename(columns={'price_asset1':'price'}, inplace = True)
print(result)
result.to_csv('btc_signals.csv', index=False)
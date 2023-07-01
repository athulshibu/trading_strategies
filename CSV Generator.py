from binance.client import Client
import pandas as pd

api_key = 'Enter_an_API_Key'
api_secret = 'Enter_the_secret_API_Key'
client = Client(api_key, api_secret)

startdate = '1 Jun, 2023'
enddate = '30 Jun, 2023'
asset1 = 'BTC'
asset2 = 'ETH'
asset1_symbol = asset1 + 'USDT'
asset2_symbol = asset2 + 'USDT'
interval = Client.KLINE_INTERVAL_1MINUTE

asset1_klines = client.get_historical_klines(asset1_symbol, interval, startdate, enddate)
asset2_klines = client.get_historical_klines(asset2_symbol, interval, startdate, enddate)



timestamps = [kline[0] for kline in asset1_klines]
highs = [float(kline[2]) for kline in asset1_klines]
lows = [float(kline[3]) for kline in asset1_klines]
prices = [float(kline[4]) for kline in asset1_klines]

asset1_data = {'Timestamp': timestamps, 'price': prices, 'high': highs, 'low': lows}
asset1_dataframe = pd.DataFrame(asset1_data)

asset1_dataframe['Timestamp'] = pd.to_datetime(asset1_dataframe['Timestamp'], unit='ms')

asset1_dataframe.to_csv(asset1.lower() + '_price_data.csv', index=False)






timestamps = [kline[0] for kline in asset2_klines]
highs = [float(kline[2]) for kline in asset2_klines]
lows = [float(kline[3]) for kline in asset2_klines]
prices = [float(kline[4]) for kline in asset2_klines]

asset2_data = {'Timestamp': timestamps, 'price': prices, 'high': highs, 'low': lows}
asset2_dataframe = pd.DataFrame(asset2_data)

asset2_dataframe['Timestamp'] = pd.to_datetime(asset2_dataframe['Timestamp'], unit='ms')

asset2_dataframe.to_csv(asset2.lower() + '_price_data.csv', index=False)

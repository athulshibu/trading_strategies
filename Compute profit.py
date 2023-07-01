import pandas as pd

df = pd.read_csv('btc_signals.csv')

initial_capital = 10000  # Starting portfolio value
position = 0 
portfolio_value = initial_capital

for index, row in df.iterrows():
    signal = row['signal']
    price = row['price']

    position_change = signal - position
    current_position = position + position_change
    position_value = current_position * price

    if index > 0:
        position_diff = position_value - previous_position_value

        portfolio_value += position_diff

    previous_position_value = position_value
    position = current_position

profit_loss = portfolio_value - initial_capital

print("Profit:", profit_loss)
print("Final Portfolio Value:", portfolio_value)

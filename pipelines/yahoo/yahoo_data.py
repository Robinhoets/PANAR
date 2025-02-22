import yfinance as yf
import pandas as pd

# Fetch U.S. Treasury yield data from yfinance
tickers = ['^IRX', '^FVX', '^TNX', '^TYX']  # 3-month, 5-year, 10-year, and 30-year Treasury yield indices
data = yf.download(tickers, start='2020-01-01', end='2021-01-01')

# Rename columns for clarity
# data.columns = ['3M', '5Y', '10Y', '30Y']

# Display the first few rows of data
print(data)
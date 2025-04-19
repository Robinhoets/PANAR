import yfinance as yf
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

'''
# Fetch U.S. Treasury yield data from yfinance
tickers = ['^IRX', '^FVX', '^TNX', '^TYX']  # 3-month, 5-year, 10-year, and 30-year Treasury yield indices
data = yf.download(tickers, start='2020-01-01', end='2021-01-01')
# Rename columns for clarity
# data.columns = ['3M', '5Y', '10Y', '30Y']
# Display the first few rows of data
print(data)
'''
def get_price_chart(ticker_chars):
    # Fetch historical price data using yfinance
    stock_data = yf.Ticker(ticker_chars)
    price_chart_data = stock_data.history(period='1y')
    return price_chart_data

def get_risk_free_rate():
    # Fetch the 10-year Treasury yield
    treasury_yield = yf.Ticker('^TNX').info['regularMarketPrice']
    # Convert to decimal
    risk_free_rate = treasury_yield / 100
    return risk_free_rate

def get_beta(ticker_chars):
    # Fetch beta value using yfinance
    company = yf.Ticker(ticker_chars)
    # Get beta value
    beta = company.info.get('beta')
    return beta

def get_shares_outstanding(ticker_chars):
    # Fetch shares outstanding using yfinance
    company = yf.Ticker(ticker_chars)
    shares_outstanding = company.info.get('sharesOutstanding')
    return shares_outstanding

def get_market_price(ticker_chars):
    # Fetch market price using yfinance
    company = yf.Ticker(ticker_chars)
    market_price = company.info.get('currentPrice')
    return market_price
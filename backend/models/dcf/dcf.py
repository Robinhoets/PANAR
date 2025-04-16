from datetime import datetime
import requests
import os
import pandas as pd
import numpy as np
import unicodedata
import json
from matplotlib import pyplot as plt
import csv
from pipelines.yahoo.yahoo import *
from pipelines.risk_premiums import get_equity_risk_premium

def coe(rf_rate, beta, equity_risk_premium):
    # Calculate the cost of equity using the Capital Asset Pricing Model (CAPM)
    return beta * equity_risk_premium

def dcf_model(future_net_income, COE, PGR, shares_outstanding, market_price):
    #TODO: use formula to get from net income to fcf
    fcf = future_net_income
    #print("Future Free Cash Flows:")
    #print(fcf)
    #print("Discount Rate (Cost of Equity):", COE*100, "%")
    #print("Perpetual Growth Rate:", PGR*100, "%")
    #print("----------------------------------------------------")
    quarterly_COE = (1 + COE) ** (1/4) - 1
    quarterly_PGR = (1 + PGR) ** (1/4) - 1

    last_quarter = fcf.iloc[0, len(fcf.columns) - 1]
    for i in range(0,len(fcf.columns)):
        fcf.iloc[0,i] = int(fcf.iloc[0,i] / (1 + quarterly_COE) ** (i + 1))
    discount_fcf = fcf
    #print("Discounted Free Cash Flows:")
    #print(discount_fcf)
    if last_quarter < 0:
        terminal_value = 0
        pv_of_tv = 0
    else:
        terminal_value = int(last_quarter * (1 + quarterly_PGR) / (quarterly_COE - quarterly_PGR))
        #print("Terminal value at", PGR*100, "% growth per year and discounting by", COE * 100, "% per year: ",terminal_value)
        pv_of_tv = int(terminal_value / (1 + quarterly_COE) ** (len(fcf.columns) + 1))
    #print("Present value of terminal value: ", pv_of_tv)
    pv_of_cf = int(discount_fcf.iloc[0].sum())
    if(pv_of_cf < 0):
        pv_of_cf = 0
    #print("Present value of cash flows: ", pv_of_cf)
    presant_value = int(pv_of_cf + pv_of_tv)
    #print("Total present value of cash flows and terminal value: ", presant_value)

    price_per_share = presant_value / shares_outstanding
    #print("Estimated Price per share: ", price_per_share)
    #print("Actual Price per share: ", market_price)

    percent_return = (price_per_share - market_price) / market_price * 100
    #print("Implied Premium/discount: ", percent_return, "%")
    dcf_dictionary = {
        "discount_rate": str(round(COE * 100, 2)) + "%",
        "perpetual_growth_rate": str(PGR * 100) + "%",
        "terminal_value": "$"+ str(int(terminal_value)),
        "present_value_of_terminal_value": "$" + str(int(pv_of_tv)),
        "present_value_of_cash_flows": "$" + str(int(pv_of_cf)),
        "present_value": "$" + str(int(presant_value)),
        "value_per_share": price_per_share,
        "market_price": market_price,
        "implied_premium": str(round(percent_return,2)) + "%",
    }
    return dcf_dictionary

def dcf(future_net_income, ticker):
    COE = coe(get_risk_free_rate, get_beta(ticker), get_equity_risk_premium())
    shares_outstanding = get_shares_outstanding(ticker)
    market_price = get_market_price(ticker)
    #needs formulae
    PQR = .02
    return dcf_model(future_net_income, COE, PQR, shares_outstanding, market_price)
#main test

#dcf(fcf, COE, PGR, shares_outstanding, market_price)
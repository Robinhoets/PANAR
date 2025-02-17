from datetime import datetime
import requests
import os
import pandas as pd
import numpy as np
import urllib.request, urllib.error, urllib.parse
import re
from bs4 import BeautifulSoup, UnicodeDammit
import unicodedata
import json
from matplotlib import pyplot as plt
from pathlib import Path

email = ""

def getCIKs():
    """
    This function retrieves all the tickers on the SEC website and returns them in a dataframe
    """
    headers = {'User-Agent': f"{email}"}
    companyTickers = requests.get(
        "https://www.sec.gov/files/company_tickers.json",
        headers=headers
        )
    CIKDict = companyTickers.json()
    
    #Dictionary to dataframe convserion
    CIKs = pd.DataFrame(index = range(len(CIKDict)), columns = ["CIK", "Ticker", "Name"])
    for i in range(len(CIKDict)): 
        CIKs.iloc[i, 0] = str(CIKDict[str(i)]['cik_str']).zfill(10)
        CIKs.iloc[i, 1] = CIKDict[str(i)]['ticker']
        CIKs.iloc[i, 2] = CIKDict[str(i)]['title']
    return CIKs
    
class Company():
    
    #2023 is the year that the program will start loading in financial reports, this can be changed to any year but it takes a very long time to 
    #import all the data
    def __init__(self, ticker):
        self.ticker = ticker
        self.cik = self.findCik()

    def findCik(self):
        cikRow = tickerDf[tickerDf['Ticker'] == self.ticker]
        cik = cikRow.iloc[0, 0]
        return cik
    
    def getCik(self):
        return self.cik 

#Main
#Nesecary data that each instance of company class shares
email = "anthonytaylor@ufl.edu"
tickerDf = getCIKs()

#Comapny
intc = Company("INTC")

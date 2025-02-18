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
#import ace_tools as tools

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
    
    #Class that represents each comapny which contains raw data and financial statements 
    def __init__(self, ticker):
        self.ticker = ticker
        self.cik = self.findCik()
        self.companyFacts = self.retrieveCompanyFacts()

    def findCik(self):
        cikRow = tickerDf[tickerDf['Ticker'] == self.ticker]
        cik = cikRow.iloc[0, 0]
        return cik
    
    def getCik(self):
        return self.cik 
    
    def retrieveCompanyFacts(self):
        """
        This function retrieves the company facts 
        """
        companyFacts = requests.get(
            f'https://data.sec.gov/api/xbrl/companyfacts/CIK{self.cik}.json',
            headers={'User-Agent': email})
        companyFacts = companyFacts.json()
        return companyFacts['facts']['us-gaap']
    
    def displayLineItemNames(self):
        for lineItem in self.companyFacts.keys():
            print(lineItem)
                              
def createItemDict(companyFacts, keys):
    '''
    use regex to form condensed dictionary of just income statement items 
    '''
    dict = {}
    #Search each possible keyWord with each item in the data until match is found
    keys = [re.compile(key) for key in keys]
    for keyWord in keys:
        for key in companyFacts:
            if keyWord.search(key):
                dict[key] = companyFacts[key]
    return dict

def consolidateDict(revenueDict):
    '''
    Consolidate multiple Dictionary entries into one by choosing the longest and most reliable entries
    '''
    return revenueDict  

def createItemRow(companyFacts, keys):
    '''
    Convert item dict to item row
    '''
    itemDict = createItemDict(companyFacts, keys)
    itemDict = consolidateDict(itemDict)
    #chnage name to revenue
    keyWord = list(itemDict.keys())[0]
    itemList = itemDict[keyWord]['units']['USD']
    #create start dates, end dates, values lists
    startList = []
    endList = []
    valList = []
    for i in itemList:
        startList.append(i['start'])
        endList.append(i['end'])
        valList.append(i['val'])
    #create dataframe
    itemRow = {
        'start' : startList,
        'end' : endList,
        'Revenue' : valList
    }
    itemRow = pd.DataFrame(itemRow)
    return itemRow.T

#Main
#Nesecary data that each instance of company class shares
email = "tonytaylor25@yahoo.com"
tickerDf = getCIKs()

#Company
intc = Company("INTC")

#list line items
#intc.displayLineItemNames()

#Line item keywords
Revenue = [r"Revenues", r"SalesRevenueNet"] 
COGS = [r"CostOfGoodsSold", r'CostOfRevenue', r'CostOfGoodsAndServicesSold']
GrossProfit = [r"GrossProfit"]
OperatingExpenses = [r"[Oo]perating[Ee]xpenses"]
NetIncome = [r"\b[Nn]et[Ii]ncome[Ll]oss"]

#get item row from companyfacts
Revenue = createItemRow(intc.companyFacts, Revenue)
COGS = createItemRow(intc.companyFacts, COGS)
GrossProfit = createItemRow(intc.companyFacts, GrossProfit)
OperatingExpenses = createItemRow(intc.companyFacts, OperatingExpenses)
NetIncome = createItemRow(intc.companyFacts, NetIncome)
print(Revenue)
print(COGS)
print(GrossProfit)
print(OperatingExpenses)
print(NetIncome)

Revenue.to_csv('output.csv', index=False)

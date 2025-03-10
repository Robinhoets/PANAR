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
        'start_date' : startList,
        'end_date' : endList,
        'value' : valList
    }
    itemRow = pd.DataFrame(itemRow)
    return itemRow.T

#seperate functions that clean dataframe
def within_10_days(date1, date2):
    """
    Returns True if date1 and date2 (datetime-like) differ by at most 10 days
    when ignoring the year AND allowing wrap-around across the year boundary.
    For example, Dec 25 and Jan 1 are treated as only 7 days apart.
    """
    if pd.isnull(date1) or pd.isnull(date2):
        return False
    
    # Extract month/day, convert to a day-of-year number
    # We'll assume a non-leap-year 365-day cycle for simplicity.
    # Alternatively, you can handle leap years more precisely if desired.
    def day_of_year_non_leap(dt):
        # A quick way is to replace the year with 2001 (a non-leap year),
        # then compute dt.dayofyear. Another approach is to do a custom calculation.
        temp = dt.replace(year=2001)  # 2001 was not a leap year
        return temp.dayofyear
    
    doy1 = day_of_year_non_leap(date1)
    doy2 = day_of_year_non_leap(date2)
    
    direct_diff = abs(doy2 - doy1)
    # "Wrap" difference (circular) - treat day 365 and day 1 as neighbors
    wrap_diff = 365 - direct_diff
    
    min_diff = min(direct_diff, wrap_diff)
    
    return min_diff <= 10

def pop_one_years_worth(df):
    #min_date has to be the start date of a quarter 1
    min_date = df['start_date'].min()
    #Get all entries in the same year

    first_end_date = df.loc[df['start_date'] == min_date, 'end_date'].iloc[0]
    first_end_date = pd.to_datetime(first_end_date)
    year = first_end_date.year

    entries_within_year = df[df['end_date'].dt.year == year]
    df = df[df['end_date'].dt.year != year]
    return df, entries_within_year

def check_Q_list(df_row):
    if((df_row['start_date'].month == 1 or df_row['start_date'].month == 12)):
        if(df_row['end_date'].month == 3 or df_row['end_date'].month == 4):
            return [1]
        elif(df_row['end_date'].month == 6 or df_row['end_date'].month == 7):
            return [1,2]
        elif(df_row['end_date'].month == 9 or df_row['end_date'].month == 10):
            return [1,2,3]
        elif(df_row['end_date'].month == 12):
            return [1,2,3,4]  
    elif(df_row['start_date'].month == 4 or df_row['start_date'].month == 3):
        if(df_row['end_date'].month == 6 or df_row['end_date'].month == 7):
            return [2]
        elif(df_row['end_date'].month == 9 or df_row['end_date'].month == 10):
            return [2,3]
        elif(df_row['end_date'].month == 12):
            return [2,3,4]
    elif(df_row['start_date'].month == 6 or df_row['start_date'].month == 7):
        if(df_row['end_date'].month == 9 or df_row['end_date'].month == 10):
            return [3]
        elif(df_row['end_date'].month == 12):
            return [3,4]
    elif(df_row['start_date'].month == 9 or df_row['start_date'].month == 10):
        if(df_row['end_date'].month == 12):
            return [4]
        
def index_df_by_q_column(quarter_entries, quarter_list):
    df_out = quarter_entries.iloc[0:0]
    for index in range(0, len(quarter_entries)):
        if(quarter_entries['quarter_list'].iloc[index] == quarter_list):
            df_out = quarter_entries.iloc[index].to_frame().T
            return df_out

def get_n_sized_quarter_entries(quarter_entries, n):
    df_out = quarter_entries.iloc[0:0]
    for index in range(0, len(quarter_entries)):
        if(len(quarter_entries.iloc[index]['quarter_list']) == n):
            df_out = pd.concat([df_out, quarter_entries.iloc[index].to_frame().T], ignore_index=True)
    return df_out

def create_df_for_quarter(year, quarter, value):
    if(quarter == 1):
        df_out = {
            "start_date": pd.to_datetime([f"{year}-01-01"]),
            "end_date": pd.to_datetime([f"{year}-03-31"]),
            "value": value,
            "quarter_list": [[1]]
        }
    elif(quarter == 2):
        df_out = {
            "start_date": pd.to_datetime([f"{year}-04-01"]),
            "end_date": pd.to_datetime([f"{year}-06-30"]),
            "value": value,
            "quarter_list": [[2]]
        }
    elif(quarter == 3):
        df_out = {
            "start_date": pd.to_datetime([f"{year}-07-01"]),
            "end_date": pd.to_datetime([f"{year}-09-30"]),
            "value": value,
            "quarter_list": [[3]]
        }
    elif(quarter == 4):
        df_out = {
            "start_date": pd.to_datetime([f"{year}-10-01"]),
            "end_date": pd.to_datetime([f"{year}-12-31"]),
            "value": value,
            "quarter_list": [[4]]
        }
    return pd.DataFrame(df_out)


def clear_non_quarters(entries_for_FY):
    entries_for_FY = entries_for_FY[entries_for_FY['quarter_list'].apply(lambda x: len(x) == 1)]
    return entries_for_FY

def drop_duplicates(quarter_entries):
    df_out = quarter_entries.iloc[0:0]
    four_quarter_list = [[1], [2], [3], [4]]
    for q in four_quarter_list:
        for index in range(0, len(quarter_entries)):
            if(quarter_entries.iloc[index]['quarter_list'] == q):
                df_out = pd.concat([df_out, quarter_entries.iloc[index].to_frame().T], ignore_index=True)
                break
    return df_out

def convert_year_to_quarters(entries_for_FY):
    year_entry = get_n_sized_quarter_entries(entries_for_FY, 4)
    year = year_entry["end_date"].values[0].year
    #No data for entire year
    if(len(year_entry) == 0):
        return year_entry
    avg_item = year_entry["value"].values/4
    df_out = {
        "start_date": pd.to_datetime([f"{year}-01-01", f"{year}-04-01", f"{year}-07-01", f"{year}-10-01"]),
        "end_date": pd.to_datetime([f"{year}-03-31", f"{year}-06-30", f"{year}-09-30", f"{year}-12-31"]),
        "value": [avg_item, avg_item, avg_item, avg_item],
        "quarter_list": [[1], [2], [3], [4]]
    }
    return df_out

def convert_two_quaters_to_one(entries_for_FY, q):
    #intialize empty df
    df_out = entries_for_FY
    one_quarter_entries = get_n_sized_quarter_entries(entries_for_FY, 1)
    two_quarter_entries = get_n_sized_quarter_entries(entries_for_FY, 2)
    qlists =  two_quarter_entries['quarter_list']
    qlists_with_q = [qlist for qlist in qlists if q in qlist]
    if(len(qlists_with_q) == 0):
        #same df
        return df_out
    else:
        for qlist in qlists_with_q:
            single_two_quarter_entry = index_df_by_q_column(two_quarter_entries, qlist)
            single_one_quarter_entry = index_df_by_q_column(one_quarter_entries, [q])
            value_to_del = single_two_quarter_entry["value"][0]
            year = single_two_quarter_entry["end_date"].values[0].year
            new_q_value = single_two_quarter_entry["value"][0] - single_one_quarter_entry["value"][0]
            if q in qlist:
                qlist.remove(q)
            new_q = qlist[0]
            #remove 2 quarter entry
            df_out = df_out[df_out['value'] != value_to_del]
            df_pre_out = create_df_for_quarter(year, new_q, new_q_value)
            df_out = pd.concat([df_out, df_pre_out], ignore_index=True)
            return df_out

def quarterly_df(entries_for_FY):
    one_quarter_entries = get_n_sized_quarter_entries(entries_for_FY, 1)
    print("one quarter entries")
    print(one_quarter_entries)
    two_quarter_entries = get_n_sized_quarter_entries(entries_for_FY, 2)
    print("two quarter entries")
    print(two_quarter_entries)
    if(len(one_quarter_entries) == 0):
        df_out = convert_year_to_quarters(entries_for_FY)
        return df_out
    elif(len(one_quarter_entries) > 0 and len(two_quarter_entries) > 0):
        df_out = entries_for_FY
        for i in range(0, len(one_quarter_entries)):
            q = one_quarter_entries['quarter_list'].iloc[i][0]
            df_out = convert_two_quaters_to_one(df_out, q)
        return quarterly_df(df_out)
    elif(len(one_quarter_entries) >= 3):
        df_out = entries_for_FY
        year_entry = get_n_sized_quarter_entries(entries_for_FY, 4)
        year = year_entry["end_date"].values[0].year
        new_q_value = year_entry['value'][0]
        #delete year
        df_out = df_out[df_out['value'] != new_q_value]
        #clear non quarters
        df_out = clear_non_quarters(df_out)
        df_out = df_out.drop_duplicates(subset='value')
        df_out = drop_duplicates(df_out)
        four_quarter_list = [[1], [2], [3], [4]]
        for q in df_out['quarter_list']:
            four_quarter_list.remove(q)
        new_q = four_quarter_list[0][0]
        for value in df_out['value']:
            new_q_value = new_q_value - value
        q_entry = create_df_for_quarter(year, new_q, new_q_value)
        df_out = pd.concat([df_out, q_entry], ignore_index=True)
        return df_out.sort_values(by='start_date').reset_index(drop=True)

def consolidate_into_quarters(raw_historical_statements):
    #Get Dataeframe ready
    #convert to datetime
    raw_historical_statements['start_date'] = pd.to_datetime(raw_historical_statements['start_date'])
    raw_historical_statements['end_date']   = pd.to_datetime(raw_historical_statements['end_date'])
    #Sort
    raw_historical_statements.drop_duplicates(inplace=True)
    raw_historical_statements = raw_historical_statements.sort_values(
        by=['start_date', 'end_date'],
        ascending=[True, True]
    ).reset_index(drop=True)
    historical_statements = raw_historical_statements.iloc[0:0]
    print(raw_historical_statements)
    raw_historical_statements, entries_for_FY = pop_one_years_worth(raw_historical_statements)
    while(len(raw_historical_statements) > 4):
        raw_historical_statements, entries_for_FY = pop_one_years_worth(raw_historical_statements)

        #add qlists
        entries_for_FY["quarter_list"] = entries_for_FY.apply(check_Q_list, axis=1)

    
        print(entries_for_FY)
        print("start")
        entries_for_FY = quarterly_df(entries_for_FY)
        print("end")
        print(entries_for_FY)

        historical_statements = pd.concat([historical_statements, entries_for_FY], ignore_index=True)
    return historical_statements

def merge(statement, lineitem2):
    value_name = lineitem2.columns[2]
    statement[value_name] = pd.NA
    index1 = 0
    index2 = 0

    while(index1 < len(statement) and index2 < len(lineitem2)):
        if(statement['end_date'].iloc[index1].year == lineitem2['end_date'].iloc[index2].year):
            if(statement['quarter_list'].iloc[index1] == lineitem2['quarter_list'].iloc[index2]):
                statement[value_name].iloc[index1] = lineitem2[value_name].iloc[index2]
                index1 += 1
                index2 += 1
        else:
            return statement
    return statement
    #add functionality to add the rest of the values
#Main
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
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



Revenue = consolidate_into_quarters(Revenue.T)
COGS = consolidate_into_quarters(COGS.T)
GrossProfit = consolidate_into_quarters(GrossProfit.T)
OperatingExpenses = consolidate_into_quarters(OperatingExpenses.T)
NetIncome = consolidate_into_quarters(NetIncome.T)

#unique item names
Revenue = Revenue.rename(columns={'value': 'revenue'})
COGS = COGS.rename(columns={'value': 'cogs'})
GrossProfit = GrossProfit.rename(columns={'value': 'gross_profit'})
OperatingExpenses = OperatingExpenses.rename(columns={'value': 'operating_expenses'})
NetIncome = NetIncome.rename(columns={'value': 'net_income'})

#merge lineitems
statement = merge(Revenue, COGS)
statement = merge(statement, GrossProfit)
statement = merge(statement, OperatingExpenses)
statement = merge(statement, NetIncome)

print(statement.T)

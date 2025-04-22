from datetime import datetime, timedelta
import requests
import os
import pandas as pd
import numpy as np
import re
import json
import csv

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
        self.starting_quarter = 1

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
    
    def display_all_lineitem_names(self):
        for lineItem in self.companyFacts.keys():
            print(lineItem)
    
    def set_company_starting_quarter(self, starting_quarter):
        self.starting_quarter = starting_quarter

    def get_company_starting_quarter(self):
        return self.starting_quarter
                              
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
    if(itemDict == {}):
        return pd.DataFrame()
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

def create_Q_list2(df_row):
    if((df_row['start_date'].month == df_row['end_date'].month)):
        return [1,2,3,4]
    elif((df_row['start_date'].month == 1 or df_row['start_date'].month == 12)):
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
    else:
        raise ValueError("Non standard quarter")
       
def create_Q_list(df_row, real_quarter_one):
    staring_quarter = check_starting_quarter_of_year(df_row)
    quarter_offset = staring_quarter - real_quarter_one
    start_date = df_row['start_date'].month
    end_date = df_row['end_date'].month
    diff = (end_date - start_date) % 12
    if(quarter_offset >= 0):
        if(abs(diff) < 2 or abs(diff) > 10):
            return [1,2,3,4]
        elif((diff >=2 and diff <= 4) or (diff <= -8 and diff >= -10)):
            return [1 + quarter_offset]
        elif((diff >=5 and diff <= 7) or (diff <= -5 and diff >= -7)):
            return [1 + quarter_offset, 2 + quarter_offset]
        elif((diff >=8 and diff <= 10) or (diff <= -2 and diff >= -4)):
            return [1 + quarter_offset, 2 + quarter_offset, 3 + quarter_offset]
        else:
            raise ValueError("Non standard quarter")  
    else:
        if(abs(diff) < 2 or abs(diff) > 10):
            return [1,2,3,4]
        elif((diff >=2 and diff <= 4) or (diff <= -8 and diff >= -10)):
            return [5 + quarter_offset]
        elif((diff >=5 and diff <= 7) or (diff <= -5 and diff >= -7)):
            return [5 + quarter_offset, 5 + quarter_offset + 1]
        elif((diff >=8 and diff <= 10) or (diff <= -2 and diff >= -4)):
            return [5 + quarter_offset, (5 + quarter_offset + 1) % 4, (5 + quarter_offset + 2) % 4]
        else:
            raise ValueError("Non standard quarter")

def index_df_by_q_column(quarter_entries, quarter_list):
    df_out = quarter_entries.iloc[0:0]
    for index in range(0, len(quarter_entries)):
        if(quarter_entries['quarter_list'].iloc[index] == quarter_list):
            df_out = quarter_entries.iloc[index].to_frame().T
            return df_out

def get_n_sized_quarter_entries(quarter_entries, n):
    #if
    df_out = quarter_entries.iloc[0:0]
    for index in range(0, len(quarter_entries)):
        if(len(quarter_entries.iloc[index]['quarter_list']) == n):
            df_out = pd.concat([df_out, quarter_entries.iloc[index].to_frame().T], ignore_index=True)
    return df_out

def create_df_for_quarter(year, quarter, value):
    starting_quarter = company.get_company_starting_quarter()
    diff = quarter - starting_quarter
    q_val = 1
    if(starting_quarter == 1):
      q_val = quarter
    else:  
        q_val = (quarter + (starting_quarter - 1)) % 4
    if(q_val == 0):
        q_val = 4
    if(1 == q_val):
        df_out = {
            "start_date": pd.to_datetime([f"{year}-01-01"]),
            "end_date": pd.to_datetime([f"{year}-03-31"]),
            "value": value,
            "quarter_list": [[quarter]]
        }
    elif(2 == q_val):
        df_out = {
            "start_date": pd.to_datetime([f"{year}-04-01"]),
            "end_date": pd.to_datetime([f"{year}-06-30"]),
            "value": value,
            "quarter_list": [[quarter]]
        }
    elif(3 == q_val):
        df_out = {
            "start_date": pd.to_datetime([f"{year}-07-01"]),
            "end_date": pd.to_datetime([f"{year}-09-30"]),
            "value": value,
            "quarter_list": [[quarter]]
        }
    elif(4 == q_val):
        df_out = {
            "start_date": pd.to_datetime([f"{year}-10-01"]),
            "end_date": pd.to_datetime([f"{year}-12-31"]),
            "value": value,
            "quarter_list": [[quarter]]
        }
    return pd.DataFrame(df_out)


def clear_non_quarters(entries_for_FY):
    entries_for_FY = entries_for_FY[entries_for_FY['quarter_list'].apply(lambda x: len(x) == 1)]
    return entries_for_FY

def drop_duplicates_quarter_entries(quarter_entries):
    df_out = quarter_entries.iloc[0:0]
    four_quarter_list = [[1], [2], [3], [4]]
    for q in four_quarter_list:
        for index in range(0, len(quarter_entries)):
            if(quarter_entries.iloc[index]['quarter_list'] == q):
                df_out = pd.concat([df_out, quarter_entries.iloc[index].to_frame().T], ignore_index=True)
                break
    return df_out

def drop_duplicate_entries_based_on_qlist(quarter_entries):
    list_of_qlist_presences = []
    present = False
    for index in range(0, len(quarter_entries)):
        for qlist in list_of_qlist_presences:
            if(quarter_entries.loc[index, 'quarter_list'] == qlist):
                present = True
                break
        if(not present):
            list_of_qlist_presences.append(quarter_entries.loc[index, 'quarter_list'])
        if(present):
            quarter_entries.drop(index=index, inplace=True)
            present = False
            continue
    return quarter_entries
        

    four_quarter_list = [[1], [2], [3], [4]]
    for q in four_quarter_list:
        for index in range(0, len(quarter_entries)):
            if(quarter_entries.iloc[index]['quarter_list'] == q):
                df_out = pd.concat([df_out, quarter_entries.iloc[index].to_frame().T], ignore_index=True)
                break
    return df_out

def convert_year_to_quarters(entries_for_FY):
    year_entry = get_n_sized_quarter_entries(entries_for_FY, 4)
    starting_quarter = check_starting_quarter_of_year(year_entry)
    starting_date = year_entry["start_date"].values[0]
    end_date = year_entry["end_date"].values[0]
    #No data for entire year
    if(len(year_entry) == 0):
        return year_entry
    avg_item = int((year_entry["value"].values/4).item())
    df_out = {
        "start_date": pd.to_datetime([
            starting_date,
            starting_date + timedelta(days=91),
            starting_date + timedelta(days=181),
            starting_date + timedelta(days=271)
        ]),
        "end_date": pd.to_datetime([
            starting_date + timedelta(days=90),
            starting_date + timedelta(days=180),
            starting_date + timedelta(days=270),
            end_date
        ]),
        "value": [avg_item, avg_item, avg_item, avg_item],
        "quarter_list": [[1], [2], [3], [4]]
    }
    return pd.DataFrame(df_out)

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

def consolidate_one_FY(entries_for_FY):
    entries_for_FY = entries_for_FY.reset_index(drop=True)
    entries_for_FY = drop_duplicate_entries_based_on_qlist(entries_for_FY)
    #print(entries_for_FY)
    one_quarter_entries = get_n_sized_quarter_entries(entries_for_FY, 1)
    #print("one quarter entries")
    #print(one_quarter_entries, '\n')
    two_quarter_entries = get_n_sized_quarter_entries(entries_for_FY, 2)
    #print("two quarter entries")
    #print(two_quarter_entries, '\n')
    if(len(one_quarter_entries) == 0):
        df_out = convert_year_to_quarters(entries_for_FY)
        return df_out
    elif(len(one_quarter_entries) > 0 and len(two_quarter_entries) > 0):
        df_out = entries_for_FY
        for i in range(0, len(one_quarter_entries)):
            q = one_quarter_entries['quarter_list'].iloc[i][0]
            df_out = convert_two_quaters_to_one(df_out, q)
        return consolidate_one_FY(df_out)
    elif(len(one_quarter_entries) == 3):
        df_out = entries_for_FY
        year_entry = get_n_sized_quarter_entries(entries_for_FY, 4)
        if(len(year_entry) == 0):
            return one_quarter_entries
        else:
            year = year_entry["end_date"].values[0].year
        new_q_value = year_entry['value'][0]
        #delete year
        df_out = df_out[df_out['value'] != new_q_value]
        #clear non quarters
        df_out = clear_non_quarters(df_out)
        df_out = df_out.drop_duplicates(subset='value')
        df_out = drop_duplicates_quarter_entries(df_out)
        four_quarter_list = [[1], [2], [3], [4]]
        for q in df_out['quarter_list']:
            four_quarter_list.remove(q)
        new_q = four_quarter_list[0][0]
        for value in df_out['value']:
            new_q_value = new_q_value - value
        q_entry = create_df_for_quarter(year, new_q, new_q_value)
        df_out = pd.concat([df_out, q_entry], ignore_index=True)
        return df_out.sort_values(by='start_date').reset_index(drop=True)
    elif(len(one_quarter_entries) == 4):
        return one_quarter_entries

def check_starting_quarter_of_year(entries_for_FY):
    if isinstance(entries_for_FY, pd.Series):
        min_date = entries_for_FY['start_date']
    else:
        min_date = entries_for_FY['start_date'].min()
        
    if((min_date.month == 12 or min_date.month == 1 or min_date.month == 2)):
        return 1
    elif((min_date.month == 3 or min_date.month == 4 or min_date.month == 5)):
        return 2
    elif((min_date.month == 6 or min_date.month == 7 or min_date.month == 8)):
        return 3
    elif((min_date.month == 9 or min_date.month == 10 or min_date.month == 11)):
        return 4
    else:
        raise ValueError("Non standard quarter")
    
def pop_one_FY(df):
    #TODO: add safety if there is no 10k
    #yearly filing has to be at the beginning of frame
    yearly_filing = df['start_date'].min()
    #Get all entries in the same year

    year_end_date = df.loc[df['start_date'] == yearly_filing, 'end_date'].iloc[0]

    entries_within_year = df[df['end_date'] <= year_end_date]
    df = df[df['end_date'] > year_end_date]
    return df, entries_within_year

def consolidate_all_FY(all_entries):
    '''
    Function takes dataframe containing all historical quarterly, two-quarterly, three-quarterly, and annual filing entries for a single line item of a company
    and converts it into a dataframe containing non-redundent quarterly entries of the line item
    '''
    if(all_entries.empty):
        return all_entries
    #Get Dataeframe ready
    #convert to datetime
    all_entries['start_date'] = pd.to_datetime(all_entries['start_date'])
    all_entries['end_date']   = pd.to_datetime(all_entries['end_date'])
    #Sort by filing date and drop duplicate entries
    all_entries.drop_duplicates(inplace=True)
    all_entries = all_entries.sort_values(
        by=['start_date', 'end_date'],
        ascending=[True, False]
    ).reset_index(drop=True)
    #print("All entries")
    #print(all_entries, "\n")
    #new empty dataframe to put consolidated FY entries into
    consolidated_entries = all_entries.iloc[0:0]
        #print all given entries 
        #print(raw_historical_statements)
    #pops/removes a FY of entries from all_entries
        #TODO: this logic needs to be changed as to not waste the first parital/full FY of entries  
    #all_entries, entries_for_FY = pop_one_FY(all_entries)
    #loop will greater than 4 entries remain in all_entries 
        #TODO: this logic needs to be changed to include a final FY which is a partial FY 
    all_entries, entries_for_FY = pop_one_FY(all_entries)
    starting_quarter_for_year = check_starting_quarter_of_year(entries_for_FY)
    company.set_company_starting_quarter(starting_quarter_for_year)
    while(len(all_entries) > 4):
        #pops/removes a FY of entries from all_entries
        #add qlists data struture as a column
        #print("Pre Q List")
        #print(entries_for_FY)
        entries_for_FY["quarter_list"] = entries_for_FY.apply(create_Q_list,args=(starting_quarter_for_year,), axis=1)
        #print("Post Q list")
        #print(entries_for_FY)
        
        #print("pre-consolidated entries for FY ")
        #print(entries_for_FY, '\n')
        #consolidate FY entries of varying quarter size into 4, 1 quarter entries
        consolidated_entries_for_FY = consolidate_one_FY(entries_for_FY)
        #print("consolidated entries for FY(4 X 1 quarter entries) for FY ")
        #print(consolidated_entries_for_FY)
        #print("-------------------------------------------------------\n")
        #print("-------------------------------------------------------")
        
        #add one FY of consolidated entries to the consolidated entries dataframe
        consolidated_entries = pd.concat([consolidated_entries, consolidated_entries_for_FY], ignore_index=True)
        #pops/removes a FY of entries from all_entries
        all_entries, entries_for_FY = pop_one_FY(all_entries)
    #return all consolidated FY's by the loop 
    #Clean for merging
    if(not consolidated_entries.empty):
        consolidated_entries['Quarter'] = consolidated_entries.pop('quarter_list').apply(lambda x: x[0])
        consolidated_entries['start_date'] = pd.to_datetime(consolidated_entries['start_date'])
        consolidated_entries['end_date'] = pd.to_datetime(consolidated_entries['end_date'])
        consolidated_entries['start_date'] = consolidated_entries['start_date'].dt.strftime('%Y-%m-%d')
        consolidated_entries['end_date'] = consolidated_entries['end_date'].dt.strftime('%Y-%m-%d')
        consolidated_entries["YearAndQuarter"] = consolidated_entries["end_date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").strftime("%Y")) + "Q" + consolidated_entries["Quarter"].astype(str)
        #consolidated_entries = consolidated_entries.drop('end_date', axis=1)
        #consolidated_entries = consolidated_entries.drop('start_date', axis=1)
        consolidated_entries = consolidated_entries.drop('Quarter', axis=1)
        #consolidated_entries = consolidated_entries.drop_duplicates(subset='YearAndQuarter', keep='first')
    return consolidated_entries

def add_lineitem_to_statement(statement, lineitem):
    '''
    Merges a value column from lineitem into statement using YearAndQuarter.
    If statement is empty, return lineitem.
    If lineitem is empty, return statement.
    '''
    if statement.empty:
        return lineitem.copy()
    if lineitem.empty:
        return statement.copy()

    end_dates_col = pd.DataFrame()
    if(len(statement) >= len(lineitem)):
        end_dates_col['end_date'] = statement['end_date']
    else:
        end_dates_col['end_date'] = lineitem['end_date']
        
    value_col = lineitem.columns[2]
    statement['_original_order'] = range(len(statement))
    statement = pd.merge(statement, lineitem[['YearAndQuarter', value_col]],
                         on='YearAndQuarter', how='outer', sort=False)
    statement = statement.sort_values('_original_order').drop(columns=['_original_order']).reset_index(drop=True)
    statement['end_date'] = end_dates_col['end_date']
    statement = statement.sort_values(
        by=['end_date'],
        ascending=[True]
    ).reset_index(drop=True)
    return statement

def get_income_statement(ticker):
    #pre
    email = "tonytaylor25@yahoo.com"
    tickerDf = getCIKs()
    global company
    company = Company(ticker.upper())

    #company.display_all_lineitem_names()

    #Line item keywords
    Revenue = [r"Revenues", r"SalesRevenueNet", r"SalesRevenueServicesGross"] 
    COGS = [r"CostOfGoodsSold", r'CostOfRevenue', r'CostOfGoodsAndServicesSold']
    GrossProfit = [r"GrossProfit"]
    OperatingExpenses = [r"[Oo]perating[Ee]xpenses"]
    NetIncome = [r"\b[Nn]et[Ii]ncome[Ll]oss"]

    #get item row from companyfacts
    Revenue = createItemRow(company.companyFacts, Revenue)
    COGS = createItemRow(company.companyFacts, COGS)
    GrossProfit = createItemRow(company.companyFacts, GrossProfit)
    OperatingExpenses = createItemRow(company.companyFacts, OperatingExpenses)
    NetIncome = createItemRow(company.companyFacts, NetIncome)



    Revenue = consolidate_all_FY(Revenue.T)
    COGS = consolidate_all_FY(COGS.T)
    GrossProfit = consolidate_all_FY(GrossProfit.T)
    OperatingExpenses = consolidate_all_FY(OperatingExpenses.T)
    NetIncome = consolidate_all_FY(NetIncome.T)
    
    #unique item names
    Revenue = Revenue.rename(columns={'value': 'revenue'})
    COGS = COGS.rename(columns={'value': 'cogs'})
    GrossProfit = GrossProfit.rename(columns={'value': 'gross_profit'})
    OperatingExpenses = OperatingExpenses.rename(columns={'value': 'operating_expenses'})
    NetIncome = NetIncome.rename(columns={'value': 'net_income'})    

    statement = add_lineitem_to_statement(Revenue, COGS)
    statement = add_lineitem_to_statement(statement, GrossProfit)
    statement = add_lineitem_to_statement(statement, OperatingExpenses)
    statement = add_lineitem_to_statement(statement, NetIncome)
    '''
    #convert
    statement['Quarter'] = statement.pop('quarter_list').apply(lambda x: x[0])
    statement['start_date'] = pd.to_datetime(statement['start_date'])
    statement['end_date'] = pd.to_datetime(statement['end_date'])
    statement['start_date'] = statement['start_date'].dt.strftime('%Y-%m-%d')
    statement['end_date'] = statement['end_date'].dt.strftime('%Y-%m-%d')
    statement["YearAndQuarter"] = statement["end_date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").strftime("%Y")) + "Q" + statement["Quarter"].astype(str)
    '''
    #drop dates and NA
    statement['Quarter'] = statement['YearAndQuarter'].apply(lambda x: int(x[-1]))
    #statement = statement.drop('end_date', axis=1)
    statement = statement.drop('start_date', axis=1)
    statement = statement.replace({np.nan: None})
    statement["ticker"] = company.ticker
    return statement

def statement_to_csv(all_statements):
        all_statements.to_csv('all_statement.csv')
        
def statement_to_json(statement, company):
    statement = statement.replace({np.nan: None})

    json_data = {
        "ticker": company.ticker,
        "income_statement": statement.to_dict(orient='records')
    }
    with open('company.json', 'w') as f:
        json.dump(json_data, f, indent=2)    

def ticker_csv_to_statements():
    all_statements = pd.DataFrame(columns=["revenue", "cogs", "gross_profit", "operating_expenses", "net_income", "Quarter", "YearAndQuarter", "ticker"])
    with open("backend/tickers.csv", newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            ticker = row[0]
            statement = get_income_statement(ticker)
            all_statements = pd.concat([all_statements, statement], axis=0, ignore_index=True)
            print(all_statements)
    statement_to_csv(all_statements)
    
            

    
    

#Main     
pd.set_option('display.width', None)   
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
#Nesecary data that each instance of company class shares
email = "tonytaylor25@yahoo.com"
tickerDf = getCIKs()



#statement = get_income_statement("MA")
#print(statement)

#ticker_csv_to_statements()








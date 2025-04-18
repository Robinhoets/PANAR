'''
beaapi?

    -GDP*
    -GDP by industry*:                        [done]
    -Consumer Spending*: 
    -Personal income*                         [done]      
    -Personal Savings Rate*
    -Corporate Profits*                         
    -GDI(gross domestic income)
    -employment by industry
    -international transactions:             [working on] _ don't do
    -Government receipts and expenditures*   [done]   
    -Fixed assets by type:
    -industry fixed assets                   [working on]
    -government fixed assets
'''
import beaapi
from secret import secret
from pprint import PrettyPrinter, pprint
import pandas as pd

key = secret.get_bea_secret()
pp = PrettyPrinter(width=-1)


class Bea:
    def __init__(self):
        pass

    def get_gdp_by_industry(self):
        """ Get GDP by Industry
        
        Each line of data frame is a code, followed by the Gross Output for a Quarter. The range of 
        data is 2005 Quarter I through 2024 Quarter III. Note GDP is by quarter because montly isn't available.

        :param: None
        
        :return: Pandas Dataframe
        """
        # Set up columns and years available
        gdp_df = pd.DataFrame(columns=['Industry Code',
                                       '2005-1','2005-2','2005-3','2005-4',
                                       '2006-1','2006-2','2006-3','2006-4',
                                       '2007-1','2007-2','2007-3','2007-4',
                                       '2008-1','2008-2','2008-3','2008-4',
                                       '2009-1','2009-2','2009-3','2009-4',
                                       '2010-1','2010-2','2010-3','2010-4',
                                       '2011-1','2011-2','2011-3','2011-4',
                                       '2012-1','2012-2','2012-3','2012-4',
                                       '2013-1','2013-2','2013-3','2013-4',
                                       '2014-1','2014-2','2014-3','2014-4',
                                       '2015-1','2015-2','2015-3','2015-4',
                                       '2016-1','2016-2','2016-3','2016-4',
                                       '2017-1','2017-2','2017-3','2017-4',
                                       '2018-1','2018-2','2018-3','2018-4',
                                       '2019-1','2019-2','2019-3','2019-4',
                                       '2020-1','2020--2','2020-3','2020-4',
                                       '2021-1','2021-2','2021-3','2021-4',
                                       '2022-1','2022-2','2022-3','2022-4',
                                       '2023-1','2023-2','2023-3','2023-4',
                                       '2024-1','2024-2','2024-3'])
        years = [2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024]

        # logic: first loop: each industry code
        #        second loop: each year
        #        final: flatten column and create dataframe
        
        list_of_param_vals = beaapi.get_parameter_values(key, 'GDPbyIndustry', 'Industry')
        industry_code = list_of_param_vals['Key']
        for code in industry_code:
            print(code)
            row = [code]
            for year in years:
                try:
                    bea_tbl = beaapi.get_data(key, datasetname='GDPbyIndustry', Industry=code, Frequency='Q', TableID=15, Year=year)                          
                    data_value = bea_tbl['DataValue']
                    for val in data_value:
                        row.append(val)
                except beaapi.beaapi_error.BEAAPIResponseError:
                    print("bea response error")
                    break
            if(len(row) == len(gdp_df.columns)):
                gdp_df.loc[len(gdp_df)] = row
                print(row)
            else:
                print("row skipped")
    
        # Save DataFrame to CSV
        gdp_df.to_csv('gdp_by_industry.csv', index=False)
        return gdp_df
  
    def get_gdp_by_industry(self):
            """ 

            1925-2023
            :param: None
            
            :return: Pandas Dataframe
            """
            bea_tbl = beaapi.get_data(key, datasetname='FixedAssets', TableName='FAAt101', Year=1925)
            pp.pprint(bea_tbl)


    def get_international_transactions(self):
        international_trans_df = pd.DataFrame(columns=['Country','1960','1961','1962','1963',
                                                       '1964','1965','1966','1967',
                                                       '1968','1969','1970','1971',
                                                       '1972','1973','1974','1975',
                                                       '1976','1977','1978','1979',
                                                       '1980','1981','1982','1983',
                                                       '1984','1985','1986','1987',
                                                       '1988','1989','1990','1991',
                                                       '1992','1993','1994','1995',
                                                       '1996','1997','1998','1999',
                                                       '2000','2001','2002','2003',
                                                       '2004','2005','2006','2007',
                                                       '2008','2009','2010','2011',
                                                       '2012','2013','2014','2015',
                                                       '2016','2017','2018','2019',
                                                       '2020','2021','2022','2023',
                                                       '2024'])
        indicators = ['BalCapAcct', 'BalCurrAcct', 'BalGds', 'BalGdsServ',
                       'BalPrimInc', 'BalSecInc', 'BalServ', 'CapTransPayAndOthDeb',
                       'CapTransRecAndOthCred', 'CompOfEmplPay', 'CompOfEmplRec',
                       'CurrAndDepAssets', 'CurrAndDepAssetsCentralBank',
                       'CurrAndDepAssetsDepTaking', 'CurrAndDepAssetsOthFinNonFin',
                       'CurrAndDepLiabs', 'CurrAndDepLiabsCentralBank',
                       'CurrAndDepLiabsDepTaking', 'CurrAndDepLiabsFoa',
                       'CurrAndDepLiabsOthFinNonFin', 'CurrAndDepReserveAssets',
                       'CurrAssets', 'CurrLiabs']
        list_aoc = beaapi.get_parameter_values(key, 'ITA', 'AreaOrCountry')
        list_aoc = list_aoc['Key']

        for ind in indicators:
            print(ind)
            for aoc in list_aoc:
                print(aoc)
                row = [aoc]
                for year in range(1960, 2025):
                    try:
                        bea_tbl = beaapi.get_data(key, datasetname='ITA', Indicator=ind, AreaOrCountry=aoc, Frequency='A', Year=year)
                        data_value = bea_tbl['DataValue']
                        print(data_value)
                        for val in data_value:
                            row.append(val)
                    except beaapi.beaapi_error.BEAAPIResponseError:
                        row.append(0)
                        # print("bea response error")
                        pass
                if(len(row) == len(international_trans_df.columns)):
                    international_trans_df.loc[len(international_trans_df)] = row
                    print(row)
                else:
                    print(row)
                    print(len(row))
                    print(len(international_trans_df.columns))
                    print("row skipped")
            # Define dynamic filename
            filename = f"intl_trans_{aoc}.csv"
            # Save DataFrame to CSV
            international_trans_df.to_csv(filename, index=False)
            return international_trans_df
#'BalAcc', 
    def get_gdp(self):
        columns = []
        vals = []
        for year in range(1947, 2025):
            print(year)
            bea_tbl = beaapi.get_data(key, datasetname='NIPA', TableName='T10105', Frequency='Q', Year=year)
            gdp_per_year = bea_tbl.loc[bea_tbl['LineDescription'] == 'Gross domestic product']
            for index, quarter in gdp_per_year.iterrows():
                amount = quarter['DataValue']
                vals.append(amount)
                q = quarter['TimePeriod']
                columns.append(q)
            print(columns)
            print(vals)
        print(len(columns))
        print(len(vals))
        df = pd.DataFrame(columns = columns)
        # df.columns = columns
        df.loc[0] = vals
        df.to_csv('gdp.csv', index=False)
        return df

    def get_personal_income(self):
            bea_tbl = beaapi.get_data(key, datasetname='NIPA', TableName='T20100', Frequency='q', Year='all')
            per = bea_tbl.loc[bea_tbl['LineDescription'] == 'Personal income']
            columns = per['TimePeriod']
            vals = per['DataValue']
            print(vals.values)
            print(len(columns))
            print(len(vals))
            df = pd.DataFrame(columns = columns)
            df.loc[1] = vals.values
            df.to_csv('personal-income.csv', index=False)
            print(df)
            return df
    
    def get_current_receipts(self):
        bea_tbl = beaapi.get_data(key, datasetname='NIPA', TableName='T30100', Frequency='q', Year='all')
        per = bea_tbl.loc[bea_tbl['LineDescription'] == 'Current receipts']
        columns = per['TimePeriod']
        vals = per['DataValue']
        print(vals.values)
        print(len(columns))
        print(len(vals))
        df = pd.DataFrame(columns = columns)
        df.loc[1] = vals.values
        df.to_csv('current-receipts.csv', index=False)
        print(df)
        return df
    
    def get_corporate_profits(self):
        bea_tbl = beaapi.get_data(key, datasetname='NIPA', TableName='T61600B', Frequency='q', Year='all')
        
        per = bea_tbl.loc[bea_tbl['LineDescription'] == 'Corporate profits with inventory valuation and capital consumption adjustments']
        columns = per['TimePeriod']
        vals = per['DataValue']
        print(vals.values)
        print(len(columns))
        print(len(vals))
        df = pd.DataFrame(columns = columns)
        df.loc[1] = vals.values
        df.to_csv('corporate-profits.csv', index=False)
        print(df)
        return df



        # row_identifier = bea_tbl['LineDescription'].unique()
        # first = row_identifier[0]
        # second = bea_tbl[bea_tbl['LineDescription'] == first]
        # columns = second['TimePeriod']
        # df = pd.DataFrame(columns = columns)
        # df.insert(0, 'Identifier','')
        # for iden in row_identifier:
        #     tmp_df = bea_tbl[bea_tbl['LineDescription'] == iden]
        #     vals = tmp_df['DataValue']
        #     print(len(vals))
        #     print(len(columns))
            # pd.concat([pd.Series([iden]), vals])
            # df.loc[len(df)] = vals.values


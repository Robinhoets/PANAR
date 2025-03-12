'''
beaapi?

    -GDP*
    -GDP by industry*:          [done]
    -Consumer Spending*: 
    -Personal income*
    -Personal Savings Rate*
    -Corporate Profits*
    -GDI(gross domestic income)
    -employment by industry
    -international transactions: 
    -Government receipts and expenditures*
    -Fixed assets by type:
    -industry fixed assets
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
  

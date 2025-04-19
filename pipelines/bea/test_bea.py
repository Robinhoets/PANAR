from bea import Bea
import pandas as pd
# test = Bea()
# test.get_personal_income()
# df = test.get_gdp_by_industry()
# print(df)
# test.get_international_transactions()
# test.get_gdp()
# test.get_current_receipts()
# test.get_corporate_profits()

import beaapi
from secret import secret
from pprint import PrettyPrinter, pprint
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)

key = secret.get_bea_secret()
pp = PrettyPrinter(width=-1)


list_of_sets = beaapi.get_data_set_list(key)
pprint(list_of_sets)


list_of_params = beaapi.get_parameter_list(key, 'ITA')
pp.pprint(list_of_params)
list_of_param_vals = beaapi.get_parameter_values(key, 'ITA', 'Indicator')
pp.pprint(list_of_param_vals)



##############################################
###NIPA
# list_of_params = beaapi.get_parameter_list(key, 'NIPA')
# pp.pprint(list_of_params)

# #tableid and tablename are the same thing
# list_of_param_vals = beaapi.get_parameter_values(key, 'NIPA', 'TableName')
# pp.pprint(list_of_param_vals)

# bea_tbl = beaapi.get_data(key, datasetname='NIPA', TableName='T20100', Frequency='q', Year='all')

# # pp.pprint(bea_tbl)
# print(bea_tbl.loc[bea_tbl['LineDescription'] == 'Personal income'])

# print(bea_tbl.head(5))

# bea_tbl = beaapi.get_data(key, datasetname='NIPA', TableName='T30200', Frequency='q', Year='all')
# print(bea_tbl.loc[bea_tbl['LineDescription'] == 'Current receipts'])

# bea_tbl = beaapi.get_data(key, datasetname='NIPA', TableName='T61600B', Frequency='q', Year='all')
# print(bea_tbl.loc[bea_tbl['LineDescription'] == 'Current receipts'])
# print(bea_tbl['LineDescription'].unique())


# xxx  GDP =T10105 
# xxx  Personal Income and Its Disposition, Monthly (Q) = T20100     T20600 (M)
# xxx  Corporate profits by industry T61600A, T61600B, T61600C, T61600D
# xxx  Government Current Receipts and Expenditures T30200, T30300, T30400   T30100 (Q)
##############################################

# list_of_params = beaapi.get_parameter_list(key, 'NIPA')
# pp.pprint(list_of_params)
# list_of_params = beaapi.get_parameter_list(key, 'FixedAssets')
# pp.pprint(list_of_params)
# list_of_params = beaapi.get_parameter_list(key, 'ITA')
# pp.pprint(list_of_params)

############################################################################################

# list_of_param_vals = beaapi.get_parameter_values(key, 'GDPbyIndustry', 'Industry')

# # print("")
# # list_of_param_vals = beaapi.get_parameter_values(key, 'GDPbyIndustry', 'Year')
# pp.pprint(list_of_param_vals)
# list_of_param_vals = beaapi.get_parameter_values(key, 'FixedAssets', 'TableName')
# pp.pprint(list_of_param_vals)
# list_of_param_vals = beaapi.get_parameter_values(key, 'FixedAssets', 'Year')
# pp.pprint(list_of_param_vals)
# filtered_df = list_of_param_vals[list_of_param_vals['TableName'] == 'FAAt102' ]
# pp.pprint(filtered_df)
# # print(list_of_param_vals['Key'])

# list_of_param_table = beaapi.get_parameter_values(key, 'GDPbyIndustry', 'TableID')
# pp.pprint(list_of_param_table)

# list_of_param_vals = beaapi.get_parameter_values(key, 'ITA', 'AreaOrCountry')
# list_of_param_vals.to_csv("testing.csv")
# pp.pprint(list_of_param_vals)
# intr = beaapi.get_data(key, datasetname='ITA', Indicator='BalCapAcct', AreaOrCountry='Africa', Frequency='A', Year=2020)
# pp.pprint(intr)

################################################################################################################

# bea_tbl = beaapi.get_data(key, datasetname='GDPbyIndustry', Industry="111CA", Frequency='Q', TableID=15, Year=2005)
# pp.pprint(bea_tbl)
# bea_tbl = beaapi.get_data(key, datasetname='FixedAssets', TableName='FAAt101', Year=1925)
# # pp.pprint(bea_tbl)
# print(bea_tbl)

# bea_tbl = beaapi.get_data(key, datasetname='ITA', Indicator="BalGds")
# pp.pprint(bea_tbl)

# import json
# mjson = '[{"start_date":"2008-01-01","end_date":"2008-03-31","revenue":9673000000,"cogs":4466000000,"gross_profit":5207000000,"operating_expenses":3145000000,"net_income":1443000000,"Quarter":1},{"start_date":"2008-03-29","end_date":"2008-06-28","revenue":9470000000,"cogs":4221000000,"gross_profit":5249000000,"operating_expenses":2994000000,"net_income":1601000000,"Quarter":2},{"start_date":"2008-06-29","end_date":"2008-09-27","revenue":10217000000,"cogs":4198000000,"gross_profit":6019000000,"operating_expenses":2921000000,"net_income":2014000000,"Quarter":3},{"start_date":"2008-10-01","end_date":"2008-12-31","revenue":8226000000,"cogs":3857000000,"gross_profit":4369000000,"operating_expenses":2830000000,"net_income":234000000,"Quarter":4},{"start_date":"2008-12-28","end_date":"2009-03-28","revenue":7145000000,"cogs":3907000000,"gross_profit":3238000000,"operating_expenses":2591000000,"net_income":629000000,"Quarter":1},{"start_date":"2009-03-28","end_date":"2009-06-27","revenue":8024000000,"cogs":3945000000,"gross_profit":4079000000,"operating_expenses":4091000000,"net_income":-398000000,"Quarter":2},{"start_date":"2009-06-28","end_date":"2009-09-26","revenue":9389000000,"cogs":3985000000,"gross_profit":5404000000,"operating_expenses":2825000000,"net_income":1856000000,"Quarter":3},{"start_date":"2009-10-01","end_date":"2009-12-31","revenue":10569000000,"cogs":3729000000,"gross_profit":6840000000,"operating_expenses":4343000000,"net_income":2282000000,"Quarter":4},{"start_date":"2009-12-27","end_date":"2010-03-27","revenue":10299000000,"cogs":3770000000,"gross_profit":6529000000,"operating_expenses":3081000000,"net_income":2442000000,"Quarter":1},{"start_date":"2010-03-28","end_date":"2010-06-26","revenue":10765000000,"cogs":3530000000,"gross_profit":7235000000,"operating_expenses":3254000000,"net_income":2887000000,"Quarter":2},{"start_date":"2010-06-27","end_date":"2010-09-25","revenue":11102000000,"cogs":3781000000,"gross_profit":7321000000,"operating_expenses":3185000000,"net_income":2955000000,"Quarter":3},{"start_date":"2010-10-01","end_date":"2010-12-31","revenue":11457000000,"cogs":4051000000,"gross_profit":7406000000,"operating_expenses":3383000000,"net_income":3180000000,"Quarter":4},{"start_date":"2010-12-26","end_date":"2011-04-02","revenue":12847000000,"cogs":4962000000,"gross_profit":7885000000,"operating_expenses":3727000000,"net_income":3160000000,"Quarter":1},{"start_date":"2011-04-03","end_date":"2011-07-02","revenue":13032000000,"cogs":5130000000,"gross_profit":7902000000,"operating_expenses":3967000000,"net_income":2954000000,"Quarter":2},{"start_date":"2011-07-03","end_date":"2011-10-01","revenue":14233000000,"cogs":5215000000,"gross_profit":9018000000,"operating_expenses":4233000000,"net_income":3468000000,"Quarter":3},{"start_date":"2011-10-01","end_date":"2011-12-31","revenue":13887000000,"cogs":4935000000,"gross_profit":8952000000,"operating_expenses":4353000000,"net_income":3360000000,"Quarter":4},{"start_date":"2012-01-01","end_date":"2012-03-31","revenue":12906000000,"cogs":4641000000,"gross_profit":8265000000,"operating_expenses":4455000000,"net_income":2738000000,"Quarter":1},{"start_date":"2012-04-01","end_date":"2012-06-30","revenue":13501000000,"cogs":4947000000,"gross_profit":8554000000,"operating_expenses":4722000000,"net_income":2827000000,"Quarter":2},{"start_date":"2012-07-01","end_date":"2012-09-29","revenue":13457000000,"cogs":4942000000,"gross_profit":8515000000,"operating_expenses":4674000000,"net_income":2972000000,"Quarter":3},{"start_date":"2012-10-01","end_date":"2012-12-31","revenue":13477000000,"cogs":5660000000,"gross_profit":7817000000,"operating_expenses":4662000000,"net_income":2468000000,"Quarter":4},{"start_date":"2012-12-30","end_date":"2013-03-30","revenue":12580000000,"cogs":5514000000,"gross_profit":7066000000,"operating_expenses":4547000000,"net_income":2045000000,"Quarter":1},{"start_date":"2013-03-31","end_date":"2013-06-29","revenue":12811000000,"cogs":5341000000,"gross_profit":7470000000,"operating_expenses":4751000000,"net_income":2000000000,"Quarter":2},{"start_date":"2013-06-30","end_date":"2013-09-28","revenue":13483000000,"cogs":5069000000,"gross_profit":8414000000,"operating_expenses":4910000000,"net_income":2950000000,"Quarter":3},{"start_date":"2013-10-01","end_date":"2013-12-31","revenue":13834000000,"cogs":5263000000,"gross_profit":8571000000,"operating_expenses":5022000000,"net_income":2625000000,"Quarter":4},{"start_date":"2013-12-29","end_date":"2014-03-29","revenue":12764000000,"cogs":5151000000,"gross_profit":7613000000,"operating_expenses":5103000000,"net_income":1930000000,"Quarter":1},{"start_date":"2014-03-30","end_date":"2014-06-28","revenue":13831000000,"cogs":4914000000,"gross_profit":8917000000,"operating_expenses":5073000000,"net_income":2796000000,"Quarter":2},{"start_date":"2014-06-29","end_date":"2014-09-27","revenue":14554000000,"cogs":5096000000,"gross_profit":9458000000,"operating_expenses":4918000000,"net_income":3317000000,"Quarter":3},{"start_date":"2014-10-01","end_date":"2014-12-31","revenue":14721000000,"cogs":5100000000,"gross_profit":9621000000,"operating_expenses":5168000000,"net_income":3661000000,"Quarter":4},{"start_date":"2014-12-28","end_date":"2015-03-28","revenue":12781000000,"cogs":5051000000,"gross_profit":7730000000,"operating_expenses":5115000000,"net_income":1992000000,"Quarter":1},{"start_date":"2015-03-29","end_date":"2015-06-27","revenue":13195000000,"cogs":4947000000,"gross_profit":8248000000,"operating_expenses":5352000000,"net_income":2706000000,"Quarter":2},{"start_date":"2015-06-28","end_date":"2015-09-26","revenue":14465000000,"cogs":5354000000,"gross_profit":9111000000,"operating_expenses":4919000000,"net_income":3109000000,"Quarter":3},{"start_date":"2015-10-01","end_date":"2015-12-31","revenue":14914000000,"cogs":5324000000,"gross_profit":9590000000,"operating_expenses":5291000000,"net_income":3613000000,"Quarter":4},{"start_date":"2015-12-27","end_date":"2016-04-02","revenue":13702000000,"cogs":5572000000,"gross_profit":8130000000,"operating_expenses":5562000000,"net_income":2046000000,"Quarter":1},{"start_date":"2016-04-03","end_date":"2016-07-02","revenue":13533000000,"cogs":5560000000,"gross_profit":7973000000,"operating_expenses":6655000000,"net_income":1330000000,"Quarter":2},{"start_date":"2016-07-03","end_date":"2016-10-01","revenue":15778000000,"cogs":5795000000,"gross_profit":9983000000,"operating_expenses":5521000000,"net_income":3378000000,"Quarter":3},{"start_date":"2016-10-01","end_date":"2016-12-31","revenue":16374000000,"cogs":6269000000,"gross_profit":10105000000,"operating_expenses":5579000000,"net_income":3562000000,"Quarter":4},{"start_date":"2017-01-01","end_date":"2017-04-01","revenue":14796000000,"cogs":5649000000,"gross_profit":9147000000,"operating_expenses":5548000000,"net_income":2964000000,"Quarter":1},{"start_date":"2017-04-02","end_date":"2017-07-01","revenue":14763000000,"cogs":5665000000,"gross_profit":9098000000,"operating_expenses":5271000000,"net_income":2808000000,"Quarter":2},{"start_date":"2017-07-02","end_date":"2017-09-30","revenue":16149000000,"cogs":6092000000,"gross_profit":10057000000,"operating_expenses":4942000000,"net_income":4516000000,"Quarter":3},{"start_date":"2017-10-01","end_date":"2017-12-31","revenue":17053000000,"cogs":6286000000,"gross_profit":10767000000,"operating_expenses":5372000000,"net_income":-687000000,"Quarter":4}]'
# parsed = json.loads(mjson)
# print(json.dumps(parsed, indent=4))

# import pandas as pd
# df = pd.read_csv('gdp_by_industry.csv')
# f2 = df.head(2)
# # j = f2.to_json(orient='table')
# # print(json.dumps(j, indent=4))
# json_objects = []
# for row_index, row in f2.iterrows():
#     for col_index, cell_value in enumerate(row):
#         cell_data = {
#             "row": row_index + 1,
#             "column": col_index + 1,
#             "value": cell_value
#         }
#         json_objects.append(json.dumps(cell_data))
        
# for json_obj in json_objects:
#     print(json_obj)
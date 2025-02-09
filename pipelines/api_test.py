from sec_api import QueryApi
import pprint
queryApi = QueryApi(api_key="b23563a33d441ac011d21261a3683369f5c26cd471d95664e3b35d2ff439e49f")

query = {
  "query": "ticker:TSLA AND filedAt:[2020-01-01 TO 2020-12-31] AND formType:\"10-Q\"",
  "from": "0",
  "size": "10",
  "sort": [{ "filedAt": { "order": "desc" } }]
}

filings = queryApi.get_filings(query)

# print(filings)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(filings)
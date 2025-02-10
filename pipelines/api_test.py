from sec_api import QueryApi
import pprint
from secret import secret
queryApi = QueryApi(api_key=secret.get_secret())

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
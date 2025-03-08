import requests
import pandas as pd
url = f"https://data.sec.gov/submissions/CIK0000320193.json"
header = {
  "User-Agent": "<email-address>"#, # remaining fields are optional
#    "Accept-Encoding": "gzip, deflate",
#    "Host": "data.sec.gov"
}

company_filings = requests.get(url, headers=header).json()
# print(company_filings.keys())
company_filings_df = pd.DataFrame(company_filings["filings"]["recent"])
# print(company_filings_df[company_filings_df.form == "10-K"])
access_number = company_filings_df[company_filings_df.form == "10-K"].accessionNumber.values[0].replace("-", "")

file_name = company_filings_df[company_filings_df.form == "10-K"].primaryDocument.values[0]

url = f"https://www.sec.gov/Archives/edgar/data/0000320193/{access_number}/{file_name}"
# req_content = requests.get(url, headers=header).content.decode("utf-8")


from sec_api import XbrlApi
xbrlApi = XbrlApi("<api-Key>")
xbrl_json = xbrlApi.xbrl_to_json(htm_url=url)
print(xbrl_json["StatementsOfCashFlows"])


data = xbrl_json["StatementsOfCashFlows"]
import json
with open('apple_StatementOfCashFlows_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
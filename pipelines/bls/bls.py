import requests
import pandas as pd
import json

def fetch_bls_data(series_ids, start_year, end_year, api_key=None):
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    payload = {
        "seriesid": series_ids,
        "startyear": start_year,
        "endyear": end_year
    }
    if api_key:
        payload["registrationKey"] = api_key
    response = requests.post(url, json=payload, headers={'Content-type': 'application/json'})
    response.raise_for_status()
    data = response.json()
    if data.get("status") != "REQUEST_SUCCEEDED":
        raise Exception("BLS API request did not succeed: " + str(data))
    return data

def clean_bls_data(data_json):
    records = []
    for series in data_json['Results']['series']:
        series_id = series['seriesID']
        for obs in series['data']:
            try:
                year = int(obs['year'])
                if obs['period'].startswith('M'):
                    month = int(obs['period'][1:])
                    # Convert to full month-year string
                    date_str = pd.Timestamp(year=year, month=month, day=1).strftime('%B %Y')
                else:
                    date_str = pd.Timestamp(year=year, month=1, day=1).strftime('%B %Y')
            except Exception:
                date_str = None
            records.append({
                "series_id": series_id,
                "date": date_str,
                "value": pd.to_numeric(obs['value'], errors='coerce')
            })
    df = pd.DataFrame(records)
    df = df.dropna(subset=['date']).sort_values('date')
    return df

def fetch_all_data_in_chunks(series_ids, start_year, end_year, api_key=None):
    start_year = int(start_year)
    end_year = int(end_year)
    all_dfs = []
    # Loop through in 20-year chunks to cover all years
    for year in range(start_year, end_year + 1, 20):
        chunk_start = year
        chunk_end = min(year + 19, end_year)
        print(f"Fetching data from {chunk_start} to {chunk_end}")
        data_json = fetch_bls_data(series_ids, str(chunk_start), str(chunk_end), api_key)
        df_chunk = clean_bls_data(data_json)
        all_dfs.append(df_chunk)
    if all_dfs:
        df_all = pd.concat(all_dfs, ignore_index=True).sort_values('date')
    else:
        df_all = pd.DataFrame()
    return df_all

def create_chart_data(df, series_id, title):
    series_df = df[df['series_id'] == series_id].sort_values('date')
    dates = series_df['date'].tolist()
    values = series_df['value'].tolist()
    chart_data = {
        "title": title,
        "dates": dates,
        "values": values
    }
    return chart_data

def main():
    # All the BLS series IDs:
    series_ids = [
        # Employment
        "LNS11000000",   # Civilian Labor Force (SA)
        "LNS12000000",   # Civilian Employment (SA)
        "LNS13000000",   # Civilian Unemployment (SA)
        "LNS14000000",   # Unemployment Rate (SA)
        "CES0500000002", # Total Private Avg Weekly Hours (All Emp, SA)
        "CES0500000007", # Total Private Avg Weekly Hours (Prod/Nonsup, SA)
        "CES0500000003", # Total Private Avg Hourly Earnings (All Emp, SA)
        "CES0500000008", # Total Private Avg Hourly Earnings (Prod/Nonsup, SA)

        # Productivity
        "PRS85006092",   # Output Per Hour - Nonfarm Business Productivity
        "PRS85006112",   # Nonfarm Business Unit Labor Costs
        "PRS85006152",   # Nonfarm Business Real Hourly Compensation
        "MPU4910012",    # Private Nonfarm Multifactor Productivity

        # Price Indexes
        "CUUR0000SA0",   # CPI for All Urban Consumers (CPI-U) (Unadjusted)
        "CWUR0000SA0",   # CPI for Urban Wage Earners & Clerical Workers (CPI-W) (Unadjusted)
        "EIUIR",            # Imports - All Commodities
        "EIUIQ",            # Exports - All Commodities

        # Compensation
        "CIU1010000000000A" # Employment Cost Index (ECI) Civilian (Unadjusted)
    ]
    
    # Matching labels
    label_mapping = {
        # Employment
        "LNS11000000": "Civilian Labor Force (SA)",
        "LNS12000000": "Civilian Employment (SA)",
        "LNS13000000": "Civilian Unemployment (SA)",
        "LNS14000000": "Unemployment Rate (SA)",
        "CES0500000002": "Total Private Avg Weekly Hours (All Emp, SA)",
        "CES0500000007": "Total Private Avg Weekly Hours (Prod/Nonsup, SA)",
        "CES0500000003": "Total Private Avg Hourly Earnings (All Emp, SA)",
        "CES0500000008": "Total Private Avg Hourly Earnings (Prod/Nonsup, SA)",

        # Productivity
        "PRS85006092": "Output Per Hour - Nonfarm Productivity",
        "PRS85006112": "Nonfarm Business Unit Labor Costs",
        "PRS85006152": "Nonfarm Business Real Hourly Compensation",
        "MPU4910012":  "Private Nonfarm Multifactor Productivity",

        # Price Indexes
        "CUUR0000SA0":  "CPI-U (Unadjusted)",
        "CWUR0000SA0":  "CPI-W (Unadjusted)",
        "EIUIR":        "Imports - All Commodities",
        "EIUIQ":        "Exports - All Commodities",

        # Compensation
        "CIU1010000000000A": "Employment Cost Index (ECI) Civilian (Unadj)"
    }
    
    # Set the full time range
    start_year = "1970"
    end_year = "2023"
    api_key = "7b699f2786a447e88b4bdcaada2c3960"
    
    # Fetch and merge all data in 20-year chunks
    df = fetch_all_data_in_chunks(series_ids, start_year, end_year, api_key)
    print("Combined DataFrame with all records:")
    print(df)
    
    # For each series, create and write a separate JSON file
    for series_id in series_ids:
        title = label_mapping.get(series_id, series_id)
        chart_data = create_chart_data(df, series_id, title)
        # File name based on the label
        filename = f"{title.replace(' ', '_').replace('/', '-')}.json"
        with open(filename, "w") as f:
            json.dump(chart_data, f, indent=4)
        print(f"Created JSON file: {filename}")

if __name__ == "__main__":
    main()
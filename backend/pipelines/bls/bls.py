import requests
import pandas as pd
import json

# === CONFIGURATION ===
API_KEY = "7b699f2786a447e88b4bdcaada2c3960"
START_YEAR = "1970"
END_YEAR = "2023"

# === SERIES IDs and LABELS ===
SERIES_IDS = [
    "LNS11000000", "LNS12000000", "LNS13000000", "LNS14000000",
    "CES0500000002", "CES0500000007", "CES0500000003", "CES0500000008",
    "PRS85006092", "PRS85006112", "PRS85006152", "MPU4910012",
    "CUUR0000SA0", "CWUR0000SA0", "EIUIR", "EIUIQ", "CIU1010000000000A"
]

LABEL_MAPPING = {
    "LNS11000000": "Civilian Labor Force (SA)",
    "LNS12000000": "Civilian Employment (SA)",
    "LNS13000000": "Civilian Unemployment (SA)",
    "LNS14000000": "Unemployment Rate (SA)",
    "CES0500000002": "Total Private Avg Weekly Hours (All Emp, SA)",
    "CES0500000007": "Total Private Avg Weekly Hours (Prod/Nonsup, SA)",
    "CES0500000003": "Total Private Avg Hourly Earnings (All Emp, SA)",
    "CES0500000008": "Total Private Avg Hourly Earnings (Prod/Nonsup, SA)",
    "PRS85006092": "Output Per Hour - Nonfarm Productivity",
    "PRS85006112": "Nonfarm Business Unit Labor Costs",
    "PRS85006152": "Nonfarm Business Real Hourly Compensation",
    "MPU4910012":  "Private Nonfarm Multifactor Productivity",
    "CUUR0000SA0":  "CPI-U (Unadjusted)",
    "CWUR0000SA0":  "CPI-W (Unadjusted)",
    "EIUIR":        "Imports - All Commodities",
    "EIUIQ":        "Exports - All Commodities",
    "CIU1010000000000A": "Employment Cost Index (ECI) Civilian (Unadj)"
}
# =======================

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
                month = int(obs['period'][1:]) if obs['period'].startswith('M') else 1
                date = pd.Timestamp(year=year, month=month, day=1)
            except Exception:
                continue
            records.append({
                "series_id": series_id,
                "date": date,
                "value": pd.to_numeric(obs['value'], errors='coerce')
            })
    df = pd.DataFrame(records)
    return df.dropna(subset=["date", "value"]).sort_values("date")

def fetch_all_data_in_chunks(series_ids, start_year, end_year, api_key=None):
    all_dfs = []
    for year in range(int(start_year), int(end_year) + 1, 20):
        chunk_end = min(year + 19, int(end_year))
        print(f"Fetching data from {year} to {chunk_end}")
        data_json = fetch_bls_data(series_ids, str(year), str(chunk_end), api_key)
        df_chunk = clean_bls_data(data_json)
        all_dfs.append(df_chunk)
    return pd.concat(all_dfs, ignore_index=True).sort_values("date")

def create_chart_data(df, series_id, title):
    subset = df[df["series_id"] == series_id].copy()
    if subset.empty:
        print(f"No data found for series: {series_id}")
        return {
            "title": title,
            "dates": [],
            "values": []
        }
    subset = subset.sort_values("date")
    return {
        "title": title,
        "dates": subset["date"].dt.strftime('%Y-%m-%d').tolist(),
        "values": subset["value"].tolist()
    }

def get_bls_data():
    return fetch_all_data_in_chunks(SERIES_IDS, START_YEAR, END_YEAR, API_KEY)

def main():
    df = get_bls_data()
    for sid in SERIES_IDS:
        title = LABEL_MAPPING.get(sid, sid)
        chart_data = create_chart_data(df, sid, title)
        filename = f"{title.replace(' ', '_').replace('/', '-')}.json"
        with open(filename, "w") as f:
            json.dump(chart_data, f, indent=4)
        print(f"Created JSON file: {filename}")

if __name__ == "__main__":
    main()

__all__ = ["get_bls_data", "create_chart_data", "LABEL_MAPPING"]
label_mapping = LABEL_MAPPING
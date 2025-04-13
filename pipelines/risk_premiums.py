import pandas as pd
import requests
from io import BytesIO

def get_equity_risk_premium():
    # URL of the Excel file
    url = "https://www.stern.nyu.edu/~adamodar/pc/datasets/ctryprem.xlsx"

    # Download the Excel file
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download file: {response.status_code}")

    # Load the Excel file into a pandas DataFrame
    excel_file = BytesIO(response.content)
    df = pd.read_excel(excel_file, sheet_name=0)

    # Display the first few rows to understand the structure
    print(df.head())

    # Find the row corresponding to the United States
    # Assuming the first column contains country names
    us_row = df[df.iloc[:, 0].str.strip().str.lower() == 'united states']

    if not us_row.empty:
        # Assuming the 'Equity Risk Premium' is in the third column (index 2)
        equity_risk_premium = us_row.iloc[0, 2]
        print(f"United States Equity Risk Premium: {equity_risk_premium}")
    else:
        print("United States data not found in the dataset.")
    return equity_risk_premium

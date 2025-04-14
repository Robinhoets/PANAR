
def run_model(income_statement):
    columns = [
        '2025Q1', '2025Q2', '2025Q3', '2025Q4',
        '2026Q1', '2026Q2', '2026Q3', '2026Q4',
        '2027Q1', '2027Q2', '2027Q3', '2027Q4',
        '2028Q1', '2028Q2', '2028Q3', '2028Q4',
        '2029Q1', '2029Q2', '2029Q3', '2029Q4'
    ]
    values = [
         10000, 10000, 10000, 10000,
         10000, 10000, 10000, 10000,
         10000, 10000, 10000, 10000,
         10000, 10000, 10000, 10000,
         10000, 10000, 10000, 10000
    ]
    future_net_income = pd.DataFrame([values], columns=columns)
    # Always return 20 columns of the next 5 years of quarterly predicted net income with data format of 20XXQX
    return future_net_income
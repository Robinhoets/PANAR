from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from pipelines.sec.sec import get_income_statement
from pipelines.yahoo.yahoo import *
from pipelines.risk_premiums import get_equity_risk_premium
from models.dcf.dcf import *
from models.sample_model import run_model
from pipelines.bls import get_bls_data

app = FastAPI()

class Ticker(BaseModel):
    chars: str
    model_selection : int

@app.post("/test")
async def test(ticker: Ticker):
    #get ML model data
    company_income_statement = get_income_statement(ticker.chars)
    #get bls and bea data
    #bls_data = get_bls_data()
    #get bea data = get_bea_data()
    
    #get DCF model data
    future_net_income = run_model(company_income_statement)
    risk_free_rate = get_risk_free_rate()
    beta = get_beta(ticker.chars)
    equity_risk_premium = get_equity_risk_premium()
    discount_rate = COE(risk_free_rate, beta, equity_risk_premium)
    shares_outstanding = get_shares_outstanding(ticker.chars)
    market_price = get_market_price(ticker.chars)
    dcf_model_output = dcf(future_net_income, discount_rate, .02, shares_outstanding, market_price)
    return dcf_model_output

'''
@app.post("/test")
async def test(ticker: Ticker):
    #get ML model data
    company_income_statement = get_income_statement(ticker.chars)
    #get bls and bea data
    #bls_data = get_bls_data()
    #get bea data = get_bea_data()
    
    #get DCF model data
    future_net_income = run_model(company_income_statement)
    risk_free_rate = get_risk_free_rate()
    beta = get_beta(ticker.chars)
    equity_risk_premium = get_equity_risk_premium()
    discount_rate = COE(risk_free_rate, beta, equity_risk_premium)
    shares_outstanding = get_shares_outstanding(ticker.chars)
    market_price = get_market_price(ticker.chars)
    dcf_model_output = dcf(future_net_income, discount_rate, .02, shares_outstanding, market_price)
    return dcf_model_output
'''


#ideal price_chart function
'''
@app.post("/price-chart")
async def price_chart(ticker: Ticker):
    # From yahoo
    price_chart_data = get_price_chart(ticker.chars)
    #clean price chart data
    return price_chart_data
'''

#ideal statements function
'''
@app.post("/finanical-statement")
async def get_financial_statement(ticker: Ticker):
    all_income_statements = get_all_income_statement(ticker.chars)
    all_balance_sheets = get_all_balance_sheets(ticker.chars)
    all_statements_cashflows = get_all_cash_flow_statements(ticker.chars)
    session.add(all_income_statements)
    session.add(all_balance_sheets)
    session.add(all_statements_cashflows)
    session.commit()
    return statement
'''

#ideal macroeocomic data function
'''
@app.post("/macroeconomic-data")
async def macroeconomic_data(ticker: Ticker):  
    #get bls data
    bls_data = get_bls_data()
    #get bea data
    bea_data = get_bea_data()
    session.add(bls_data)
    session.add(bea_data)
    session.commit()
    return macroeconomic_data
'''

#ideal run_model function
'''    
@app.post("/run-model")
async def run_model(ticker: Ticker):
    #get ML model data
    #get from database
    all_income_statements = session.query(IncomeStatement).filter_by(ticker=ticker.chars).all()
    ... #get all cash flow statements
    ... #get all balance sheets
    bls_data = session.query(bls).all()
    get bea data = session.query(bea).all()
    
    #get DCF model data
    future_net_income = run_model(all_income_statements, all_balance_sheets, all_statements_cashflows, bls_data, bea_data)
    risk_free_rate = get_risk_free_rate()
    beta = get_beta(ticker.chars)
    equity_risk_premium = get_equity_risk_premium()
    discount_rate = COE(risk_free_rate, beta, equity_risk_premium)
    shares_outstanding = get_shares_outstanding(ticker.chars)
    market_price = get_market_price(ticker.chars)
    dcf_model_output = dcf(future_net_income, discount_rate, .02, shares_outstanding, market_price)
    return dcf_model_output
'''
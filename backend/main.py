from pyexpat import model
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from sklearn import model_selection
from pipelines.sec.sec import get_income_statement
from pipelines.yahoo.yahoo import get_price_chart
from models.dcf.dcf import dcf
#from pipelines.bls import get_bls_data
from pipelines.bls.bls import get_bls_data, create_chart_data, label_mapping
from fastapi.middleware.cors import CORSMiddleware
import json
from models.ML_models.helper import *
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or "*" in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

current_ticker = ""

class Ticker(BaseModel):
    tick: str
    model : str

@app.post("/initialize")
async def test(ticker: Ticker):
    global current_ticker 
    current_ticker = ticker.tick
    model_selection = ticker.model
    model_selection = model_selection[-1]
    #global bea_data
    #bea_data = get_bea_data()
    #global bls_data
    #bls_data = get_bls_data()
    global company_income_statement
    company_income_statement = get_income_statement(current_ticker)
    global future_net_income
    if(model_selection == "1"):
        future_net_income = run_linear_regresion(current_ticker)
    elif(model_selection == "2"):
        future_net_income = run_gradient_boost(current_ticker)
    elif(model_selection == "3"):
        future_net_income = run_neural_network(current_ticker)
    else:
        future_net_income = pd.read_csv("data/test_future_net_income.csv")
    global dcf_model_output
    dcf_model_output = dcf(future_net_income, current_ticker)
    return dcf_model_output

@app.get("/financial-statement")
async def get_financial_statement():
    return company_income_statement.to_dict(orient='records')

@app.get("/future-net-income")
async def get_future_net_income():
    return json.loads(future_net_income.to_json())


#ideal price_chart function
@app.get("/price-chart")
async def price_chart():
    global current_ticker 
    # From yahoo
    price_chart_data = get_price_chart(current_ticker)
    #clean price chart data
    return json.loads(price_chart_data.to_json(date_format='iso'))

@app.get("/bls-data")
async def get_bls_chart_data():
    bls_df = get_bls_data()

    series_ids = list(label_mapping.keys())
    print(bls_df.head())
    print(bls_df["series_id"].unique())
    charts = {}
    for sid in series_ids:
        human = label_mapping.get(sid, sid)
        charts[sid] = create_chart_data(bls_df, sid, human)

    return charts


import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM, Dense, Input, Flatten
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from pipelines.sec.sec import get_income_statement
import numpy as np
import pandas as pd


def array_to_quarterly_df(net_income, year, quarter) -> pd.DataFrame:
    """
    Converts a NumPy array into a DataFrame with quarterly column labels starting from a given year and quarter.

    Parameters:
        arr (np.ndarray): The input array, where each column represents a quarter.
        start_year (int): The starting year (e.g., 2025).
        start_quarter (int): The starting quarter (1 to 4).

    Returns:
        pd.DataFrame: A DataFrame with columns labeled as quarters like '2025Q1', '2025Q2', etc.
    """
    num_quarters = net_income.shape[0]
    quarters = []
    year = year
    q = quarter

    for _ in range(num_quarters):
        quarters.append(f"{year}Q{q}")
        q += 1
        if q > 4:
            q = 1
            year += 1

    return pd.DataFrame([net_income], columns=quarters)

def run_model(income_statement):
    #Mirrors xGBoost data preprocessing
    dataFrame = income_statement
    dataFrame["year_cat"] = dataFrame["YearAndQuarter"].astype(str).str[:4]

    data_columns = dataFrame[["revenue", "cogs", "gross_profit", "operating_expenses", "net_income", "year_cat"]]

    #Find correlation matrix of data points
    corrMatrix = dataFrame[["revenue", "cogs", "gross_profit", "operating_expenses", "net_income", "year_cat"]].corr()
    #To print out correlation matrix, uncomment below
    #print(corrMatrix["net_income"].sort_values(ascending=False))

    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('imputer', SimpleImputer())])

    ohe = ColumnTransformer([
        ("num", pipe, list(data_columns)),
        ("cat", OneHotEncoder(), ["Quarter"])
    ])

    data_prep = ohe.fit_transform(dataFrame)

    pred_series = np.empty((0, 0))
    input_series = np.empty((0, 0))
    size = data_prep.shape[0]

    k = 0
    for i in range(4, size):
        pred_series = np.append(pred_series, data_prep[i])
        input_series = np.append(input_series, data_prep[k:i])
        k = k + 1

    #Must make 4 input + 1 prediction series for all data 
    #Want data in form (-1, 4, 1)
    input_ser = input_series.reshape(64, 4, 10)
    pred_ser = pred_series.reshape(64, 10)
    print(input_ser.shape)
    print(pred_ser.shape)

    #Custom train/test split should be done here; After all series are gathered
    input_train, input_test = train_test_split(input_ser, test_size=.2, shuffle=False)
    pred_train, pred_test = train_test_split(pred_ser, test_size=.2, shuffle=False)

    model = Sequential([
        LSTM(128, activation='relu', return_sequences=True),
        LSTM(64, activation='relu', return_sequences=True),
        LSTM(32, activation='relu', return_sequences=False),
        Dense(10)
    ])

    model.compile(optimizer='adam', loss='mse')

    model.fit(input_ser, pred_ser, epochs=150, batch_size=input_ser.shape[0], verbose=1)
    model.summary()

    #Testing of generated model based on data input 
    test = model.predict(input_test, batch_size=input_test.shape[0], verbose=1)

    performance = mean_squared_error(pred_test[:, 4], test[:, 4])
    print("RMSE: ", np.sqrt(performance))
    r2 = r2_score(pred_test[:, 4], test[:, 4])
    print("R2 score = ", r2)

    #Data preprocessing DONE after this point; now for sliding window prediction going forward 5 years (20 points total)
    #Use previous 4 quarters of data to predict new net income value; use that value with previous 3 quarters to predict value after; continue 
    future_series = np.empty((0, 0))
    working_series = np.empty((0, 0))
    starter_input = input_ser[[-4]]

    #Single starter prediction
    starter_pred = model.predict(starter_input)
    future_series = np.append(future_series, starter_pred)

    working_series = np.append(working_series, starter_input)
    working_series = np.append(working_series, starter_pred)
    working_series = working_series.reshape(5, 10)
    working_series = working_series[1:]
    working_series = working_series.reshape(1, 4, 10)

    #Predict next 19 values 
    for i in range(1, 20):
        future_pred = model.predict(working_series, batch_size=1, verbose=1)
        working_series = np.append(working_series, future_pred)
        working_series = working_series.reshape(5, 10)
        working_series = working_series[1:]
        working_series = working_series.reshape(1, 4, 10)
        future_series = np.append(future_series, future_pred)

    #Grab what you need from future series data; in this case, only net income asked for
    future_series = future_series.reshape(20, 10)
    future_series = future_series[:, [0, 1, 2, 3, 4, 5]]

    scaler = ohe.named_transformers_['num'].named_steps['scaler']
    scaled_data = scaler.inverse_transform(future_series)
    net_income = scaled_data[:, 4]
    print(net_income)

    np.savetxt("INTC_net_income_prediction.csv", net_income, delimiter=',')
    model.save("LSTM_NN_WORKING.keras")
    
    return array_to_quarterly_df(net_income, 2025, 1)
    

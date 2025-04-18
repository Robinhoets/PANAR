import tensorflow as tf
from keras._tf_keras.keras.models import Sequential
from keras._tf_keras.keras.layers import LSTM, Dense, Input, Flatten
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import numpy as np
import pandas as pd

class neuralNetwork:
    def __init__(self):
        self.model = None
        self.ohe = None
        self.input_ser = None
        self.validate_ser = None
        self.validate_train = None
        self.validate_test = None
        self.last_quarter = None
    
    def train(self, all_data):

        #Mirrors xGBoost data preprocessing
        dataFrame = pd.read_csv(all_data)
        self.last_quarter = dataFrame.iloc[-1]["YearAndQuarter"]
        
        dataFrame["year_cat"] = dataFrame["YearAndQuarter"].astype(str).str[:4]

        data_columns = dataFrame[["revenue", "cogs", "gross_profit", "operating_expenses", "net_income", "year_cat"]]

        #Find correlation matrix of data points
        corrMatrix = dataFrame[["revenue", "cogs", "gross_profit", "operating_expenses", "net_income", "year_cat"]].corr()
        #To print out correlation matrix, uncomment below
        #print(corrMatrix["net_income"].sort_values(ascending=False))

        pipe = Pipeline([
            ('scaler', StandardScaler()),
            ('imputer', SimpleImputer())])

        self.ohe = ColumnTransformer([
            ("num", pipe, list(data_columns)),
            ("cat", OneHotEncoder(), ["Quarter"])
        ])

        data_prep = self.ohe.fit_transform(dataFrame)

        validate_series = np.empty((0, 0))
        input_series = np.empty((0, 0))
        size = data_prep.shape[0]

        k = 0
        for i in range(4, size):
            validate_series = np.append(validate_series, data_prep[i])
            input_series = np.append(input_series, data_prep[k:i])
            k = k + 1

        #Must make 4 input + 1 prediction series for all data 
        #Want data in form (-1, 4, 1)
        self.input_ser = input_series.reshape(64, 4, 10)
        self.validate_ser = validate_series.reshape(64, 10)
        print(self.input_ser.shape)
        print(self.validate_ser.shape)

        #Custom train/test split should be done here; After all series are gathered
        input_train, input_test = train_test_split(self.input_ser, test_size=.2, shuffle=False)
        self.validate_train, self.validate_test = train_test_split(self.validate_ser, test_size=.2, shuffle=False)

        self.model = Sequential([
            LSTM(128, activation='relu', return_sequences=True),
            LSTM(64, activation='relu', return_sequences=True),
            LSTM(32, activation='relu', return_sequences=False),
            Dense(10)
        ])

        self.model.compile(optimizer='adam', loss='mse')

        self.model.fit(input_train, self.validate_train, epochs=150, batch_size=self.input_ser.shape[0], verbose=1)
        self.model.summary()

        #Testing of generated model based on data input 
        test = self.model.predict(input_test, batch_size=input_test.shape[0], verbose=1)

        performance = mean_squared_error(self.validate_test[:, 4], test[:, 4])
        print("RMSE: ", np.sqrt(performance))
        r2 = r2_score(self.validate_test[:, 4], test[:, 4])
        print("R2 score = ", r2)

        #Data preprocessing DONE after this point; save model and return
        self.model.save("NN_WORKING.keras")

    def predict(self, company):
        #Now format prediction for sliding window prediction going forward 5 years (20 points total)
        #Use previous 4 quarters of data to predict new net income value; use that value with previous 3 quarters to predict value after; continue 
        
        #SELECT COMPANY HERE, MUST BE IN COLUMNS SOMEWHERE
        
        future_series = np.empty((0, 0))
        working_series = np.empty((0, 0))
        starter_input = self.input_ser[[-4]]

        #Single starter prediction
        starter_pred = self.model.predict(starter_input)
        future_series = np.append(future_series, starter_pred)

        working_series = np.append(working_series, starter_input)
        working_series = np.append(working_series, starter_pred)
        working_series = working_series.reshape(5, 10)
        working_series = working_series[1:]
        working_series = working_series.reshape(1, 4, 10)

        #Predict next 19 values 
        for i in range(1, 20):
            future_pred = self.model.predict(working_series, batch_size=1, verbose=1)
            working_series = np.append(working_series, future_pred)
            working_series = working_series.reshape(5, 10)
            working_series = working_series[1:]
            working_series = working_series.reshape(1, 4, 10)
            future_series = np.append(future_series, future_pred)

        #Grab what you need from future series data; in this case, only net income asked for
        future_series = future_series.reshape(20, 10)
        future_series = future_series[:, [0, 1, 2, 3, 4, 5]]
        print(future_series[:, 4])

        scaler = self.ohe.named_transformers_['num'].named_steps['scaler']
        scaled_data = scaler.inverse_transform(future_series)
        net_income = scaled_data[:, 4]
        print(net_income)
        
        #Create future columns based on last quarter parse
        columns = []
        year = int(self.last_quarter[:4])
        quarter = int(self.last_quarter[-1])
        
        for i in range(0, 20):
            quarter += 1
            if(quarter > 4):
                quarter = 1 
                year += 1
            columns.append(f"{year}Q{quarter}")
                
        values = net_income
        future_net_income = pd.DataFrame([values], columns=columns)
        return future_net_income
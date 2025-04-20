import tensorflow
#MAY NEED TO CHANGE DEPENDENCIES FROM KERAS._TF_KERAS TO TENSORFLOW FOR RUNNING APP
from keras._tf_keras.keras.models import Sequential, load_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from keras._tf_keras.keras.layers import LSTM, Dense, BatchNormalization
from keras._tf_keras.keras.optimizers import RMSprop, Adam
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class neuralNetwork:
    def __init__(self):
        self.model = None
        self.encoder = None
        self.input_ser = None
        self.validate_ser = None
        self.validate_train = None
        self.validate_test = None
        self.last_quarter = None
        self.parameter_num = None
    
    def train(self, all_data):

        #Mirrors xGBoost data preprocessing
        dataFrame = pd.read_csv(all_data)
        self.last_quarter = dataFrame.iloc[-1]["YearAndQuarter"]
        
        dataFrame["year_ord"] = dataFrame["YearAndQuarter"].astype(str).str[:4]

        data_columns = dataFrame[["revenue", "cogs", "gross_profit", "operating_expenses", "net_income"]]

        #Find correlation matrix of data points
        corrMatrix = dataFrame[["revenue", "cogs", "gross_profit", "operating_expenses", "net_income"]].corr()
        #To print out correlation matrix, uncomment below
        #print(corrMatrix["net_income"].sort_values(ascending=False))

        pipe = Pipeline([
            ('scaler', StandardScaler()),
            ('imputer', SimpleImputer(strategy="mean"))])

        self.encoder = ColumnTransformer([
            ("num", pipe, list(data_columns)),
            ("cat", OneHotEncoder(), ["Quarter"]),
            ("ord", OrdinalEncoder(), ["year_ord", "ticker"])
        ])

        data_prep = self.encoder.fit_transform(dataFrame)
        
        self.ticker_map = {ticker: idx for idx, ticker in enumerate(self.encoder.named_transformers_["ord"].categories_[1])}
        self.parameter_num = data_prep.shape[1]

        validate_series = np.empty((0, 0))
        input_series = np.empty((0, 0))
        size = data_prep.shape[0]

        k = 0
        for i in range(4, size):
            if(data_prep[k, 10] != data_prep[i, 10]):
                k = k + 1
                continue
            validate_series = np.append(validate_series, data_prep[i])
            input_series = np.append(input_series, data_prep[k:i])
            k = k + 1

        #Must make 4 input + 1 prediction series for all data 
        #Want data in form (-1, 4, 1)
        self.input_ser = input_series.reshape(-1, 4, self.parameter_num)
        self.validate_ser = validate_series.reshape(-1, self.parameter_num)

        input_train, input_test = train_test_split(self.input_ser, test_size=.2, shuffle=False)
        self.validate_train, self.validate_test = train_test_split(self.validate_ser, test_size=.2, shuffle=False)

        self.model = Sequential([
            LSTM(128, activation='relu', return_sequences=True, dropout=0.1),
            LSTM(64, activation='relu', return_sequences=True),
            LSTM(32, activation='relu', return_sequences=False),
            Dense(11)
        ])
        
        opt = Adam(learning_rate=0.001)
        self.model.compile(optimizer=opt, loss='mse')

        self.model.fit(input_train, self.validate_train, epochs=150, batch_size=self.input_ser.shape[0])
        self.model.summary()

        #Testing of generated model based on data input 
        test = self.model.predict(input_test, batch_size=input_test.shape[0])

        performance = mean_squared_error(self.validate_test[:, 4], test[:, 4])
        print("RMSE: ", np.sqrt(performance))
        r2 = r2_score(self.validate_test[:, 4], test[:, 4])
        print("R2 score = ", r2)

        #Data preprocessing DONE after this point; save model and return
        self.model.save("backend/models/ML_models/saved_models/NN_WORKING.keras")

    def predict(self, company):
        #Now format prediction for sliding window prediction going forward 5 years (20 points total)
        #Use previous 4 quarters of data to predict new net income value; use that value with previous 3 quarters to predict value after; continue 
        #Select desired company from data
        try:
            userComp = self.ticker_map[company]
        except KeyError:
            return(f"Error: Company '{company}' not found in data. Aborting prediction.")
        
        future_series = np.empty((0, 0))
        working_series = np.empty((0, 0))
        
        tickerRows = np.array(self.input_ser)
        temp = tickerRows.reshape(-1, self.parameter_num)
        tickerAdj = temp[temp[:, 10] == userComp]
        tickerAdj = tickerAdj[-4:]
        tickerAdj = tickerAdj.reshape(-1, 4, self.parameter_num)

        #Single starter prediction
        starter_pred = self.model.predict(tickerAdj)
        future_series = np.append(future_series, starter_pred)

        working_series = np.append(working_series, tickerAdj)
        working_series = np.append(working_series, starter_pred)
        working_series = working_series.reshape(5, self.parameter_num)
        working_series = working_series[1:]
        working_series = working_series.reshape(1, 4, self.parameter_num)

        #Predict next 19 values 
        for i in range(1, 20):
            future_pred = self.model.predict(working_series, batch_size=1, verbose=1)
            working_series = np.append(working_series, future_pred)
            working_series = working_series.reshape(5, self.parameter_num)
            working_series = working_series[1:]
            working_series = working_series.reshape(1, 4, self.parameter_num)
            future_series = np.append(future_series, future_pred)

        #Grab what you need from future series data; in this case, only net income asked for
        future_series = future_series.reshape(20, self.parameter_num)
        future_series = future_series[:, [0, 1, 2, 3, 4]]

        scaler = self.encoder.named_transformers_['num'].named_steps['scaler']
        scaled_data = scaler.inverse_transform(future_series)
        net_income = scaled_data[:, 4]
        
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
    
    def PANAR_predict(self, company):
        try:
            userComp = self.ticker_map[company]
        except KeyError:
            return(f"Error: Company '{company}' not found in data. Aborting prediction.")
        
        nn = load_model("backend/models/ML_models/saved_models/NN_WORKING.keras")
        
        future_series = np.empty((0, 0))
        working_series = np.empty((0, 0))
        
        tickerRows = np.array(self.input_ser)
        temp = tickerRows.reshape(-1, self.parameter_num)
        tickerAdj = temp[temp[:, 10] == userComp]
        tickerAdj = tickerAdj[-4:]
        tickerAdj = tickerAdj.reshape(-1, 4, self.parameter_num)

        starter_pred = nn.predict(tickerAdj)
        future_series = np.append(future_series, starter_pred)

        working_series = np.append(working_series, tickerAdj)
        working_series = np.append(working_series, starter_pred)
        working_series = working_series.reshape(5, self.parameter_num)
        working_series = working_series[1:]
        working_series = working_series.reshape(1, 4, self.parameter_num)

        for i in range(1, 20):
            future_pred = nn.predict(working_series, batch_size=1, verbose=1)
            working_series = np.append(working_series, future_pred)
            working_series = working_series.reshape(5, self.parameter_num)
            working_series = working_series[1:]
            working_series = working_series.reshape(1, 4, self.parameter_num)
            future_series = np.append(future_series, future_pred)

        future_series = future_series.reshape(20, self.parameter_num)
        future_series = future_series[:, [0, 1, 2, 3, 4]]

        scaler = self.encoder.named_transformers_['num'].named_steps['scaler']
        scaled_data = scaler.inverse_transform(future_series)
        net_income = scaled_data[:, 4]
        
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
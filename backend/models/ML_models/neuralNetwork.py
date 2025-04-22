import tensorflow
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, BatchNormalization
from tensorflow.keras.optimizers import RMSprop, Adam
#MAY NEED TO CHANGE DEPENDENCIES FROM KERAS._TF_KERAS TO TENSORFLOW FOR RUNNING APP
#from keras._tf_keras.keras.models import Sequential, load_model
#from keras._tf_keras.keras.layers import LSTM, Dense, BatchNormalization
#from keras._tf_keras.keras.optimizers import RMSprop, Adam
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Initialization, training and prediction methods for neural network PANAR model
class neuralNetwork:
    def __init__(self):
        #Model needs to store values as an object for self-reference in prediction
        self.model = None
        self.encoder = None
        self.input_ser = None
        self.validate_ser = None
        self.validate_train = None
        self.validate_test = None
        self.last_quarter = "2024Q4"
        self.parameter_num = None
    
    def train(self, all_data):
        dataFrame = pd.read_csv(all_data)
        
        #Create new year column for encoding
        dataFrame["year_ord"] = dataFrame["YearAndQuarter"].astype(str).str[:4]

        data_columns = dataFrame[["revenue", "cogs", "gross_profit", "operating_expenses", "net_income"]]

        #Find correlation matrix of data points
        corrMatrix = dataFrame[["revenue", "cogs", "gross_profit", "operating_expenses", "net_income"]].corr()
        #print(corrMatrix["net_income"].sort_values(ascending=False))
        
        #Uncomment to see data heat map / correlation
        #sns.heatmap(corrMatrix, annot=True, fmt=".2f", cmap='coolwarm', center=0, linewidths=1, linecolor='black')
        #plt.title("Data Correlation")
        #plt.show()

        #Data processing pipeline
        pipe = Pipeline([
            ('scaler', StandardScaler()),
            ('imputer', SimpleImputer(strategy="mean"))])

        self.encoder = ColumnTransformer([
            ("num", pipe, list(data_columns)),
            ("cat", OneHotEncoder(), ["Quarter"]),
            ("ord", OrdinalEncoder(), ["year_ord", "ticker"])
        ])

        #Pushes data through preprocessing pipeline 
        data_prep = self.encoder.fit_transform(dataFrame)
        
        #Creates ticker mapping reference for later use in prediction
        self.ticker_map = {ticker: idx for idx, ticker in enumerate(self.encoder.named_transformers_["ord"].categories_[1])}
        self.parameter_num = data_prep.shape[1]

        validate_series = np.empty((0, 0))
        input_series = np.empty((0, 0))
        size = data_prep.shape[0]

        #Sliding prediction window 
        k = 0
        for i in range(4, size):
            if(data_prep[k, 10] != data_prep[i, 10]):
                k = k + 1
                continue
            validate_series = np.append(validate_series, data_prep[i])
            input_series = np.append(input_series, data_prep[k:i])
            k = k + 1

        #Must make 4 input + 1 prediction series for all data 
        #Want data in form (-1, 4, 11 or parameter number)
        self.input_ser = input_series.reshape(-1, 4, self.parameter_num)
        self.validate_ser = validate_series.reshape(-1, self.parameter_num)

        #Split for validation of model (usually on a single company)
        input_train, input_test = train_test_split(self.input_ser, test_size=.2, shuffle=False)
        self.validate_train, self.validate_test = train_test_split(self.validate_ser, test_size=.2, shuffle=False)

        #Neural network internal layers
        self.model = Sequential([
            LSTM(128, activation='relu', return_sequences=True, dropout=0.1),
            LSTM(64, activation='relu', return_sequences=True),
            LSTM(32, activation='relu', return_sequences=False),
            Dense(11)
        ])
        
        #Initialize model 
        opt = Adam(learning_rate=0.001)
        self.model.compile(optimizer=opt, loss='mse')

        self.model.fit(input_train, self.validate_train, epochs=150, batch_size=self.input_ser.shape[0])
        #self.model.summary()

        #Testing of generated model based on data input 
        test = self.model.predict(input_test, batch_size=input_test.shape[0])

        #Performance metrics for net income ONLY, uncomment for terminal print
        performance = mean_squared_error(self.validate_test[:, 4], test[:, 4])
        #print("RMSE: ", np.sqrt(performance))
        r2 = r2_score(self.validate_test[:, 4], test[:, 4])
        #print("R2 score = ", r2)

        #Saves current model in local directory for future access; commented out due to PANAR models already being selected
        #self.model.save("backend/models/ML_models/saved_models/NN_WORKING.keras")

    def predict(self, company):
        #Maps given company to one in given financial statements
        try:
            userComp = self.ticker_map[company]
        except KeyError:
            return(f"Error: Company '{company}' not found in data. Aborting prediction.")
        
        #Sets up prediction window of last four quarters of desired company
        future_series = np.empty((0, 0))
        working_series = np.empty((0, 0))
        
        tickerRows = np.array(self.input_ser)
        temp = tickerRows.reshape(-1, self.parameter_num)
        tickerAdj = temp[temp[:, 10] == userComp]
        tickerAdj = tickerAdj[-4:]
        tickerAdj = tickerAdj.reshape(-1, 4, self.parameter_num)

        #Predicts next quarter of net income for specific company
        starter_pred = self.model.predict(tickerAdj)
        future_series = np.append(future_series, starter_pred)

        working_series = np.append(working_series, tickerAdj)
        working_series = np.append(working_series, starter_pred)
        working_series = working_series.reshape(5, self.parameter_num)
        working_series = working_series[1:]
        working_series = working_series.reshape(1, 4, self.parameter_num)

        #Predicts 19 more quarters using sliding window prediction
        for i in range(1, 20):
            future_pred = self.model.predict(working_series, batch_size=1, verbose=1)
            working_series = np.append(working_series, future_pred)
            working_series = working_series.reshape(5, self.parameter_num)
            working_series = working_series[1:]
            working_series = working_series.reshape(1, 4, self.parameter_num)
            future_series = np.append(future_series, future_pred)

        #Reshapes data and converts it back to non-scaled format
        future_series = future_series.reshape(20, self.parameter_num)
        future_series = future_series[:, [0, 1, 2, 3, 4]]

        scaler = self.encoder.named_transformers_['num'].named_steps['scaler']
        scaled_data = scaler.inverse_transform(future_series)
        net_income = scaled_data[:, 4]
        
        #Create future columns based on last quarter parse
        columns = []
        year = int(self.last_quarter[:4])
        quarter = int(self.last_quarter[-1])
        
        #Finds next quarters of desired company's potential quarterly prediction
        for i in range(0, 20):
            quarter += 1
            if(quarter > 4):
                quarter = 1 
                year += 1
            columns.append(f"{year}Q{quarter}")
             
        #Returns net income dataframe to frontend for displaying   
        values = net_income
        future_net_income = pd.DataFrame([values], columns=columns)
        return future_net_income
    
    #Same function as predict() above, but uses PANAR hand-selected model instead of most recent training
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
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

#Initialization, training and prediction methods for linear regression PANAR model 
class linearRegression():
    def __init__(self):
        #Model needs to store values as an object for self-reference in prediction
        self.model = None
        self.encoder = None
        self.ticker_map = None
        self.last_quarter = "2024Q4"
        self.input_x = None
        self.input_y = None
        self.parameter_num = None
        
    def train(self, all_data):
        dataFrame = pd.read_csv(all_data)
        
        #Create new year column for encoding
        dataFrame["year_ord"] = dataFrame["YearAndQuarter"].astype(str).str[:4]
        
        data_columns = dataFrame[["revenue", "cogs", "gross_profit", "operating_expenses", "net_income"]]

        #Find correlation matrix of data points
        corrMatrix = dataFrame[["revenue", "cogs", "gross_profit", "operating_expenses", "net_income"]].corr()
        #print(corrMatrix["year_cat"].sort_values(ascending=False))

        #Uncomment to see data heat map / correlation
        #sns.heatmap(corrMatrix, annot=True, fmt=".2f", cmap='coolwarm', center=0, linewidths=1, linecolor='black')
        #plt.title("Data Correlation")
        #plt.show()

        #Data processing pipeline
        pipe = Pipeline([
            ('imputer', SimpleImputer(strategy="mean")), 
            ('scaler', StandardScaler())])

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

        self.input_x = []
        self.input_y = []
        size = data_prep.shape[0]
        
        #Sliding prediction window 
        k = 0
        for i in range(4, size):
            if(data_prep[k, 10] != data_prep[i, 10]):
                k = k + 1
                continue
            self.input_x.append(data_prep[k:i].flatten())
            self.input_y.append(data_prep[i])
            k = k + 1
        
        #Split for validation of model (usually on a single company)
        train_input, validate_input = train_test_split(self.input_x, test_size=0.2, shuffle=False)
        train_target, validate_target = train_test_split(self.input_y, test_size=0.2, shuffle=False)

        #Initialize model 
        lin = LinearRegression()
        self.model = lin.fit(train_input, train_target)

        #Validate model performance 
        y_validate = self.model.predict(validate_input)
        
        #Performance metrics for net income ONLY, uncomment for terminal print
        performance = mean_squared_error(validate_target, y_validate)
        #print("RMSE: ", np.sqrt(performance))
        r2 = r2_score(validate_target, y_validate)
        #print("R2 score = ", r2)
        
        #Saves current model in local directory for future access; commented out due to PANAR models already being selected
        #joblib.dump(self.model, "backend/models/ML_models/saved_models/LINEAR_WORKING.joblib")
        
    def predict(self, company):
        #Maps given company to one in given financial statements
        try:
            userComp = self.ticker_map[company]
        except KeyError:
            return(f"Error: Company '{company}' not found in data. Aborting prediction.")
        
        #Sets up prediction window of last four quarters of desired company
        future_series = np.empty((0, 0))
        working_series = np.empty((0, 0))
        
        tickerRows = np.array(self.input_x)
        temp = tickerRows[tickerRows[:, 10] == userComp]
        tickerAdj = temp[[-1]].reshape(1, -1)
        
        #Predicts next quarter of net income for specific company
        starter_pred = self.model.predict(tickerAdj)
        future_series = np.append(future_series, starter_pred)
        
        starter = tickerAdj.reshape(4, -1)
        
        working_series = np.append(working_series, starter[1])
        working_series = np.append(working_series, starter[2])
        working_series = np.append(working_series, starter[3])
        working_series = np.append(working_series, starter_pred)

        #Predicts 19 more quarters using sliding window prediction
        for i in range(1, 20):
            working_series = working_series.reshape(1, -1)
            future_pred = self.model.predict(working_series)
            working_series = working_series.reshape(4, -1)
            working_series = working_series[1:]
            working_series = np.append(working_series, future_pred)
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
        
        lin = joblib.load("backend/models/ML_models/saved_models/LINEAR_WORKING.joblib")
        
        future_series = np.empty((0, 0))
        working_series = np.empty((0, 0))
        
        tickerRows = np.array(self.input_x)
        temp = tickerRows[tickerRows[:, 10] == userComp]
        tickerAdj = temp[[-1]].reshape(1, -1)
        
        starter_pred = lin.predict(tickerAdj)
        future_series = np.append(future_series, starter_pred)
        
        starter = tickerAdj.reshape(4, -1)
        
        working_series = np.append(working_series, starter[1])
        working_series = np.append(working_series, starter[2])
        working_series = np.append(working_series, starter[3])
        working_series = np.append(working_series, starter_pred)

        for i in range(1, 20):
            working_series = working_series.reshape(1, -1)
            future_pred = lin.predict(working_series)
            working_series = working_series.reshape(4, -1)
            working_series = working_series[1:]
            working_series = np.append(working_series, future_pred)
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
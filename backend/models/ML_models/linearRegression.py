from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

class linearRegression():
    def __init__(self):
        self.model = None
        self.ohe = None
        self.last_quarter = None
        self.input_x = None
        self.input_y = None
        self.parameter_num = None
        
    def train(self, all_data):
        dataFrame = pd.read_csv(all_data)
        self.last_quarter = dataFrame.iloc[-1]["YearAndQuarter"]
        
        dataFrame["year_cat"] = dataFrame["end_date"].astype(str).str[:4]
        
        data_columns = dataFrame[["revenue", "cogs", "gross_profit", "operating_expenses", "net_income", "year_cat"]]

        #Find correlation matrix of data points
        corrMatrix = dataFrame[["revenue", "cogs", "gross_profit", "operating_expenses", "net_income", "year_cat", "Quarter"]].corr()
        #print(corrMatrix["year_cat"].sort_values(ascending=False))

        #Uncomment to see data heat map / correlation
        #sns.heatmap(corrMatrix, annot=True, fmt=".2f", cmap='coolwarm', center=0, linewidths=1, linecolor='black')
        #plt.title("Data Correlation")
        #plt.show()

        pipe = Pipeline([
            ('imputer', SimpleImputer()), 
            ('scaler', StandardScaler())])

        self.ohe = ColumnTransformer([
            ("num", pipe, list(data_columns)),
            ("cat", OneHotEncoder(), ["Quarter"])
        ])

        data_prep = self.ohe.fit_transform(dataFrame)
        
        self.parameter_num = data_prep.shape[1]

        self.input_x = []
        self.input_y = []
        size = data_prep.shape[0]
        
        k = 0
        for i in range(4, size):
            self.input_x.append(data_prep[k:i].flatten())
            self.input_y.append(data_prep[i])
            k = k + 1
        
        train_input, validate_input = train_test_split(self.input_x, test_size=0.2, shuffle=False)
        train_target, validate_target = train_test_split(self.input_y, test_size=0.2, shuffle=False)

        lin = LinearRegression()
        self.model = lin.fit(train_input, train_target)

        #Validate model performance 
        y_validate = self.model.predict(validate_input)
        
        performance = mean_squared_error(validate_target, y_validate)
        print("RMSE: ", np.sqrt(performance))
        r2 = r2_score(validate_target, y_validate)
        print("R2 score = ", r2)
        
        joblib.dump(self.model, "backend/models/saved_models/LINEAR_WORKING.joblib")
        
    def predict(self, company):
        future_series = np.empty((0, 0))
        working_series = np.empty((0, 0))
        starter_series = self.input_x[-1].reshape(1, -1)
        
        starter_pred = self.model.predict(starter_series)
        future_series = np.append(future_series, starter_pred)
        
        starter = starter_series.reshape(4, -1)
        
        working_series = np.append(working_series, starter[1])
        working_series = np.append(working_series, starter[2])
        working_series = np.append(working_series, starter[3])
        working_series = np.append(working_series, starter_pred)

        for i in range(1, 20):
            working_series = working_series.reshape(1, -1)
            future_pred = self.model.predict(working_series)
            working_series = working_series.reshape(4, -1)
            working_series = working_series[1:]
            working_series = np.append(working_series, future_pred)
            future_series = np.append(future_series, future_pred)

        future_series = future_series.reshape(20, self.parameter_num)
        future_series = future_series[:, [0, 1, 2, 3, 4, 5]]
        
        scaler = self.ohe.named_transformers_['num'].named_steps['scaler']
        scaled_data = scaler.inverse_transform(future_series)
        net_income = scaled_data[:, 4]
        print(net_income)
        
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
        lin = joblib.load("backend/models/saved_models/LINEAR_WORKING.joblib")
        
        future_series = np.empty((0, 0))
        working_series = np.empty((0, 0))
        starter_series = self.input_x[-1].reshape(1, -1)
        
        starter_pred = lin.predict(starter_series)
        future_series = np.append(future_series, starter_pred)
        
        starter = starter_series.reshape(4, -1)
        
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
        future_series = future_series[:, [0, 1, 2, 3, 4, 5]]
        
        scaler = self.ohe.named_transformers_['num'].named_steps['scaler']
        scaled_data = scaler.inverse_transform(future_series)
        net_income = scaled_data[:, 4]
        print(net_income)
        
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
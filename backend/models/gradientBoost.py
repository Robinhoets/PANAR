import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from xgboost import plot_tree

print(xgb.__version__)
print(xgb.rabit.get_rank())

class gradientBoost:
    def __init__(self):
        self.model = None
        self.ohe = None
        self.dValidate = None
        self.input_x = None
        self.input_y = None
        self.last_quarter = None
        
    def train(self, all_data):
        dataFrame = pd.read_csv(all_data)
        self.last_quarter = dataFrame.iloc[-1]["YearAndQuarter"]

        #Create new year column for encoding
        dataFrame["year_cat"] = dataFrame["end_date"].astype(str).str[:4]

        data_columns = dataFrame[["revenue", "cogs", "gross_profit", "operating_expenses", "net_income", "year_cat"]]

        #Find correlation matrix of data points
        corrMatrix = dataFrame[["revenue", "cogs", "gross_profit", "operating_expenses", "net_income"]].corr()
        print(corrMatrix["net_income"].sort_values(ascending=False))

        pipe = Pipeline([
            ('imputer', SimpleImputer()), 
            ('scaler', StandardScaler())])

        #Potential one hot encoding transformer to be added (if categorical data required)
        self.ohe = ColumnTransformer([
            ("num", pipe, list(data_columns)),
            ("cat", OneHotEncoder(), ["Quarter"])
        ])

        data_prep = self.ohe.fit_transform(dataFrame)
        
        self.input_x = []
        self.input_y = []
        size = data_prep.shape[0]
        
        k = 0
        for i in range(4, size):
            self.input_x.append(data_prep[k:i].flatten())
            self.input_y.append(data_prep[i])
            k = k + 1
            
        #MUST PREDICT NEXT VALUE. CAN NOT SHUFFLE.
        train_input, validate_input = train_test_split(self.input_x, test_size=0.2, shuffle=False)
        train_target, validate_target = train_test_split(self.input_y, test_size=0.2, shuffle=False)
        
        print(self.input_x[0])

        #Get data into xgBoost form
        dTrain = xgb.DMatrix(train_input, train_target)
        self.dValidate = xgb.DMatrix(validate_input, validate_target)

        #TODO: MUST FIND BEST PARAMETERS 
        parameters = {
            'tree_method': 'gpu_hist',
            'predictor': 'gpu_predictor',
            'objective': 'reg:squarederror',
            'device': 'gpu',
            'eval_metric': 'rmse',
            'learning_rate': 1,
            'max_depth': 4
        }

        self.model = xgb.train(parameters, dTrain)
        yPred = self.model.predict(self.dValidate)

        plot_tree(self.model)
        plt.show()

        performance = mean_squared_error(validate_target, yPred)
        print("RMSE: ", np.sqrt(performance))
        r2 = r2_score(validate_target, yPred)
        print("R2 score = ", r2)

        self.model.save_model("BOOST_WORKING.keras")

    def predict(self, company):
        future_series = np.empty((0, 0))
        working_series = np.empty((0, 0))
        starterMatrix = xgb.DMatrix(self.input_x[-1].reshape(1, -1))
        
        starter_pred = self.model.predict(starterMatrix)
        future_series = np.append(future_series, starter_pred)
        
        starter = self.input_x[-1].reshape(4, -1)
        
        working_series = np.append(working_series, starter[1])
        working_series = np.append(working_series, starter[2])
        working_series = np.append(working_series, starter[3])
        working_series = np.append(working_series, starter_pred)
        
        for i in range(1, 20):
            futureMatrix = xgb.DMatrix(working_series.reshape(1, -1))
            future_pred = self.model.predict(futureMatrix)
            working_series = working_series.reshape(4, -1)
            working_series = working_series[1:]
            working_series = np.append(working_series, future_pred)
            future_series = np.append(future_series, future_pred)
            
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
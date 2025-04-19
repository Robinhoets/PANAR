from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import seaborn as sns
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

dataFrame = pd.read_csv("intc.csv")
data_columns = dataFrame[["revenue", "cogs", "gross_profit", "operating_expenses", "net_income"]]

#Create new year column for encoding
dataFrame["year_cat"] = dataFrame["YearAndQuarter"].astype(str).str[:4]
#dataFrame["quarter_cat"] = dataFrame["quarter_list"].astype(str).str[1]

#Find correlation matrix of data points
corrMatrix = dataFrame[["revenue", "cogs", "gross_profit", "operating_expenses", "net_income", "year_cat", "Quarter"]].corr()
print(corrMatrix["year_cat"].sort_values(ascending=False))

sns.heatmap(corrMatrix, annot=True, fmt=".2f", cmap='coolwarm', center=0, linewidths=1, linecolor='black')
plt.title("Data Correlation")
plt.show()

pipe = Pipeline([
    ('imputer', SimpleImputer()), 
    ('std_scaler', StandardScaler())])

#Potential one hot encoding transformer to be added (if categorical data required)
ohe = ColumnTransformer([
    ("num", pipe, list(data_columns))
    #,
    #("cat", OneHotEncoder(), ["Quarter", "year_cat"])
])

data_prep = ohe.fit_transform(dataFrame)

##Must split in time series to avoid look-ahead
##data_train, data_test = train_test_split(data_prep, test_size=0.2)
data_train = data_prep[:40]
data_test = data_prep[40:]
#
train_target = data_train[-1, [0, 1, 2, 3]]
test_target = data_test[-1, [0, 1, 2, 3]]
#train_target = data_train[-1, [1, 2, 3, 4, 5]]
#test_target = data_test[-1, [1, 2, 3, 4, 5]]
#data_train = data_train[:-1, :]
#data_test = data_test[:-1, :]
#
#print(data_train.shape)
#print(train_target.shape)

#DON"T EVEN KNOW IF YOU CAN DO THIS WITH LINEAR REGRESSION

linReg = LinearRegression()
linReg.fit(data_train.reshape(1, -1), train_target.reshape(1, -1))

#TODO: ADAPT TO ROLLING
annual = []
for i in range(4, len(data_train)):
    window_data = data_train[i - 4:i]
    predict = linReg.predict(window_data)
    annual.append(predict)

print(annual)
#Linear Regression, not many params to use 

y_result = linReg.predict(data_test)

performance = mean_squared_error(test_target, y_result)
print("RMSE: ", np.sqrt(performance))
r2 = r2_score(y_result, test_target)
print("R2 score = ", r2)

joblib.dump(linReg, "LINEAR_WORKING.model")
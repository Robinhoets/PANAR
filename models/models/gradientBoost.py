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

dataFrame = pd.read_csv("statement.csv")
data_columns = dataFrame[["revenue", "cogs", "gross_profit", "operating_expenses", "net_income"]]

#Find correlation matrix of data points
corrMatrix = dataFrame[["revenue", "cogs", "gross_profit", "operating_expenses", "net_income"]].corr()
print(corrMatrix["net_income"].sort_values(ascending=False))

#Create new year column for encoding
dataFrame["year_cat"] = dataFrame["end_date"].astype(str).str[:4]

#pipe = Pipeline([
#    ('imputer', SimpleImputer()), 
#    ('std_scaler', StandardScaler())])

pipe = Pipeline([
    ('imputer', SimpleImputer())])

#Potential one hot encoding transformer to be added (if categorical data required)
ohe = ColumnTransformer([
    ("num", pipe, list(data_columns)),
    ("cat", OneHotEncoder(), ["quarter_list", "year_cat"])
])

data_prep = ohe.fit_transform(dataFrame)

#MUST PREDICT NEXT VALUE. CAN NOT SHUFFLE.
#data_train, data_test = train_test_split(data_prep, test_size=0.2)
data_train = data_prep[:32]
data_test = data_prep[32:]

data_train = data_train[:-1, :]
data_test = data_test[:-1, :]
train_target = data_train[:, [1, 2, 3, 4, 5]]
test_target = data_test[:, [1, 2, 3, 4, 5]]


print(data_train.shape[0])
print(train_target.shape[0])
print(data_test.shape)
print(test_target.shape)

#Get data into xgBoost form
dTrain = xgb.DMatrix(data_train, train_target)
dTest = xgb.DMatrix(data_test, test_target)

#TODO: MUST FIND BEST PARAMETERS 
parameters = {
    'objective': 'reg:squarederror',
    'device': 'cuda',
    'eval_metric': 'rmse',
    'learning_rate': 0.1,
    'max_depth': 4
}

boost = xgb.train(parameters, dTrain)
yPred = boost.predict(dTest)

plot_tree(boost)
plt.show()

performance = mean_squared_error(test_target, yPred)
print("RMSE: ", np.sqrt(performance))
r2 = r2_score(test_target, yPred)
print("R2 score = ", r2)

boost.save_model("BOOST_WORKING.model")
#boost.dump_model('dump.raw.txt', 'featmap.txt')

#Reload model
#boost = xgb.Booster({'nthread': 4})  
#boost.load_model('BOOST_97.model') 

yUser = boost.predict(dTest)
print(yUser)
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import numpy as np
import pandas as pd
import joblib

"""Potential Models:

Linear (Could be depreciated by end)
Random Forest
Singular Value Decomposition
Gradient Boost (or any tree boosting algorithm)
Neural Network

"""

dataFrame = pd.loaddata.here
data_columns = dataFrame[['all', 'input', 'columns', 'here']]

#Standard imputer to remove potential NaN and scaler for numerical values 
pipe = Pipeline([
    ('imputer', SimpleImputer()), 
    ('std_scaler', StandardScaler())])

#Potential one hot encoding transformer to be added (if categorical data required)
#ohe = ColumnTransformer([
#    ("num", pipe, list(data_columns)),
#    ("cat", OneHotEncoder(), ['insert', 'categories', 'here'])
#])

data_prep = pipe.fit_transform(dataFrame)
#data_prep = ohe.fit_transform(dataFrame)

data_train, data_test = train_test_split(data_prep, test_size=0.2)
train_target = data_train['target']
test_target = data_test['target']

#Gradient Boost Regression; max_features = columns to consider, max_depth = levels of decision tree to use  
gBoost = GradientBoostingRegressor(n_estimators=500, max_features=5, max_depth=5)
gBoost.fit(data_train, train_target)

y_result = gBoost.predict(data_test, test_target)

#Determine RSME and R2 score to judge model performance
performance = mean_squared_error(test_target, y_result)
print("Gradient Boost RMSE: ", np.sqrt(performance))
r2 = r2_score(y_result, test_target)
print("R2 score = ", r2)

#Save model with joblib
#joblib.dump(gBoost, "Gradient_Boost_PANAR_Model")
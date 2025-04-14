from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import numpy as np
import pandas as pd

dataFrame = pd.loaddata.here

#More transformers can be added later / one hot encoding if required 
pipe = Pipeline([
    ('imputer', SimpleImputer()), 
    ('std_scaler', StandardScaler())])

data_prep = pipe.fit_transform(dataFrame)
data_train, data_test = train_test_split(data_prep, test_size=0.2)

#Linear Regression, not many params to use 
linReg = LinearRegression()
linReg.fit(data_train, data_train['target'])

y_result = linReg.predict(data_test, data_test['target'])

performance = mean_squared_error(data_test['target'], y_result)
print("Gradient Boost RMSE: ", np.sqrt(performance))
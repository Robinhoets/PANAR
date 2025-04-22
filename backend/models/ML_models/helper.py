from models.ML_models.linearRegression import *
from models.ML_models.gradientBoost import *
from models.ML_models.neuralNetwork import *


def run_linear_regresion(ticker):
    #Takes whole data set as training input 
    lin = linearRegression()
    lin.train("data/all_statements.csv")

    #To predict company, provide ticker to function
    output1 = lin.predict(ticker)

    #Can also use saved generated model for prediction; pulls from same object and loads from 'saved_models' folder
    #output1 = lin.PANAR_predict("INTC")
    return output1


def run_gradient_boost(ticker):
    xgb = gradientBoost.gradientBoost()
    xgb.train("all_statements.csv")
    xgb_output = xgb.predict(ticker)
    #output2 = xgb.PANAR_predict("INTC")
    return xgb_output


def run_neural_network(ticker):
    # Create a new instance of the neuralNetwork class
    nn = neuralNetwork()
    # Train the model with the provided CSV file
    nn.train("data/all_statements.csv")
    # Predict using the trained model
    nn_output = nn.predict(ticker)
    return nn_output

#Main

'''
lin_output = run_linear_regresion(ticker)
print(lin_output)
xgb_output = run_gradient_boost(ticker)
print(xgb_output)
nn_output = run_neural_network(ticker)
print(nn_output)
'''
#from models.linearRegression import *
#from models.gradientBoost import *
from models.ML_models.neuralNetwork import *

'''
def run_linear_regresion(ticker):
    #Takes whole data set as training input 
    lin = linearRegression.linearRegression()
    lin.train("intc.csv")

    #To predict company, provide ticker to function
    output1 = lin.predict("INTC")

    #Can also use saved generated model for prediction; pulls from same object and loads from 'saved_models' folder
    #output1 = lin.PANAR_predict("INTC")
    return output1
'''
'''
def run_gradient_boost(ticker):
    xgb = gradientBoost.gradientBoost()
    xgb.train("intc.csv")
    xgb_output = xgb.predict("INTC")
    #output2 = xgb.PANAR_predict("INTC")
    return xgb_output
'''

def run_neural_network(ticker):
    # Create a new instance of the neuralNetwork class
    nn = neuralNetwork()
    # Train the model with the provided CSV file
    nn.train("data/statement.csv")
    # Predict using the trained model
    nn_output = nn.predict(ticker)
    return nn_output

#Main
ticker = "INTC"
'''
lin_output = run_linear_regresion(ticker)
print(lin_output)
xgb_output = run_gradient_boost(ticker)
print(xgb_output)
nn_output = run_neural_network(ticker)
print(nn_output)
'''
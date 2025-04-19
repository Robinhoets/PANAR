import linearRegression
import gradientBoost
import neuralNetwork

#Takes whole data set as training input 
lin = linearRegression.linearRegression()
lin.train("intc.csv")

#To predict company, provide ticker to function
output1 = lin.predict("INTC")

#Can also use saved generated model for prediction; pulls from same object and loads from 'saved_models' folder
#output1 = lin.PANAR_predict("INTC")
print(output1)

xgb = gradientBoost.gradientBoost()
xgb.train("intc.csv")
output2 = xgb.predict("INTC")
#output2 = xgb.PANAR_predict("INTC")
print(output2)

nn = neuralNetwork.neuralNetwork()
nn.train("intc.csv")
output3 = nn.predict("INTC")
#output3 = nn.PANAR_predict("INTC")
print(output3)
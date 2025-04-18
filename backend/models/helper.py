import neuralNetwork
import gradientBoost

#Takes whole data set as training input 
nn = neuralNetwork.neuralNetwork()
nn.train("intc.csv")

#To predict company, provide ticker to function
output = nn.predict("INTC")
print(output)

xgb = gradientBoost.gradientBoost()
xgb.train("intc.csv")
output = xgb.predict("INTC")
print(output)

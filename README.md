# PANAR
Pipeline - sec, bls, bea, and yahoo data retrievers. Data comes from the web and must be stored on a server. Pipeline data will be sent as both csv's to model and jsons to frontend
Model - Machine learning models create cash flow estimates for DCF model. DCF model creates stock price estimate. Model must exist on a server and receive data from pipelines. DCF model will send josn output to front end 
Frontend - Frontend will recieve jsons from server and display to user. Occasionally send back json containing user input

Instructions:
-Commit all working changes to dev when ready
-Dev will be occasionally merged with main 

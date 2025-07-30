import joblib
model=joblib.load(r"C:\Users\labuser\Downloads\CCPP.pkl")
 
import requests
 
from flask import Flask, request
import numpy as np
 
app=Flask(__name__)
@app.route('/',methods=['POST'])
 
def predictive_model():
    data=request.get_json(force=True)
    #print(data[])
    print(data)
    data=data['data']
    output=model.predict([data])
    return str(output)
 
app.run()
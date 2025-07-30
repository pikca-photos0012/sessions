import joblib
model=joblib.load(r"C:\Users\labuser\Downloads\CCPP.pkl")
 
import requests
 
from flask import Flask, request
import numpy as np
 
app=Flask(__name__)
@app.route('/',methods=['POST'])
 
def predictive_model():
    print(request.headers)
    data=request.get_json(force=True)
    print(data)
    # Extract the required fields in the specified order
    data = [
        data['temperature'],
        data['exhaust_vacuum'],
        data['ambient_pressure'],
        data['relative_humidity']
    ]
    
    print(data)

    output = model.predict([data])
    return str(output)
 
app.run()
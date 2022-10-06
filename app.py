from flask import Flask, render_template, request, jsonify
import requests
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
import datetime

app = Flask(__name__)
model = pickle.load(open('car-price.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

today = datetime.date.today()
today_year = today.year

@app.route("/",methods=['GET'])
def Home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    # Fuel_Type_Diesel=0
    if request.method == 'POST':
        year = int(request.form['year'])
        price = float(request.form['price'])
        kms_driven = int(request.form['kmsdriven'])
        owner_ = int(request.form['owners'])
        owner = owner_ - 1
        fuel_type = request.form['fueltype']
        seller_type = request.form['sellertype']
        transmission = request.form['transmission']

        year = today_year - year

        if fuel_type == 'Petrol':
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        elif fuel_type == 'Diesel':
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0
        
        if seller_type=='Individual':
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0	

        if transmission=='Manual':
            Transmission_Manual=1
        else:
            Transmission_Manual=0

        prediction=model.predict(scaler.transform([[price,kms_driven,owner,year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual]]))
        prediction = np.expm1(prediction)
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction="You can sell this car at ₹{} Lakhs".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
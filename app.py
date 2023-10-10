from flask import Flask,render_template,url_for,request,redirect,jsonify
import mysql.connector
import pickle
import numpy as np
import pandas as pd
app=Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))
ordinalencoder=pickle.load(open("ordinal.pkl","rb"))
conn=mysql.connector.connect(host="sql11.freesqldatabase.com",user="sql11646034",password="LIuFwiIjPl",database="sql11646034")
cursor=conn.cursor()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/login_validation',methods=["POST"])
def login_validation():
    email=request.form.get("email")
    password=request.form.get("Password")
    cursor.execute(""" SELECT * FROM `user1` WHERE `email` LIKE '{}' and `password` LIKE '{}' """.format(email,password))
    users=cursor.fetchall()
    if len(users)>0:
        return render_template('index.html')
    else:
        return render_template('login.html')
@app.route('/register_validation',methods=["POST"])
def register_validation():
    name=request.form.get("name")
    email=request.form.get("email")
    password=request.form.get("Password")
    cursor.execute(""" INSERT INTO `user1` (`name`,`email`,`password`) VALUES ('{}','{}','{}')""".format(name,email,password))
    conn.commit()
    return "User registered sucessfully"

@app.route("/predict", methods = ["POST"])
def predict():
     features = [[x for x in request.form.values()]]
     features1=preprocess_data(features)
     features2=preprocess_data1(features1)
     prediction = model.predict(features2)
     return render_template("index.html", prediction_text = display(prediction))

def display(data):
    if data==1:
        return "Loan is approved"
    if data==0:
        return "loan is not approved"

def preprocess_data(arr):
    from sklearn.preprocessing import OrdinalEncoder
    oe=OrdinalEncoder(categories=[["Graduate","Not Graduate"],["Yes","No"],["Urban","Semiurban","Rural"]])
    array=oe.fit_transform([arr[0][:3]])
    df4=np.hstack((array,[arr[0][3:]]))
    df4=pd.DataFrame(np.hstack((array,[arr[0][3:]])))
    a=df4.iloc[0].to_numpy()
    return a

def preprocess_data1(arr):
    from sklearn.preprocessing import PolynomialFeatures
    polynomial_features=PolynomialFeatures(degree=3)
    poly_converter=polynomial_features.fit_transform([arr])
    return poly_converter

if __name__=='__main__':
    app.run(debug=True)
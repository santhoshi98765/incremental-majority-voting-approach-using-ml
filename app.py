import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import sqlite3
import pandas as pd

import warnings

import sqlite3
import random

import smtplib 
from email.message import EmailMessage
from datetime import datetime

warnings.filterwarnings('ignore')



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/about1")
def about1():
    return render_template("about1.html")

@app.route("/about2")
def about2():
    return render_template("about2.html")

@app.route("/about3")
def about3():
    return render_template("about3.html")

@app.route("/about4")
def about4():
    return render_template("about4.html")

@app.route('/logon')
def logon():
	return render_template('register.html')

@app.route('/login')
def login():
	return render_template('login.html')


@app.route('/home1')
def home1():
	return render_template('home1.html')

@app.route('/home2')
def home2():
	return render_template('home2.html')

@app.route('/home3')
def home3():
	return render_template('home3.html')

@app.route('/home4')
def home4():
	return render_template('home4.html')


@app.route("/signup")
def signup():
    global otp, username, name, email, number, password
    username = request.args.get('user','')
    name = request.args.get('name','')
    email = request.args.get('email','')
    number = request.args.get('mobile','')
    password = request.args.get('password','')
    otp = random.randint(1000,5000)
    print(otp)
    msg = EmailMessage()
    msg.set_content("Your OTP is : "+str(otp))
    msg['Subject'] = 'OTP'
    msg['From'] = "evotingotp4@gmail.com"
    msg['To'] = email
    
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("evotingotp4@gmail.com", "xowpojqyiygprhgr")
    s.send_message(msg)
    s.quit()
    return render_template("val.html")

@app.route('/predict_lo', methods=['POST'])
def predict_lo():
    global otp, username, name, email, number, password
    if request.method == 'POST':
        message = request.form['message']
        print(message)
        if int(message) == otp:
            print("TRUE")
            con = sqlite3.connect('signup.db')
            cur = con.cursor()
            cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
            con.commit()
            con.close()
            return render_template("login.html")
    return render_template("register.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("login.html")    

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("home1.html")
    else:
        return render_template("login.html")

@app.route("/notebook1")
def notebook1():
    return render_template("NSL-KDD.html")

@app.route("/notebook2")
def notebook2():
    return render_template("KDDCUP.html")

@app.route("/notebook3")
def notebook3():
    return render_template("CICIDS2017.html")

@app.route("/notebook4")
def notebook4():
    return render_template("CICIDS2018.html")


@app.route('/predict',methods=['POST'])
def predict():
    int_features= [float(x) for x in request.form.values()]
    print(int_features,len(int_features))
    final4=[np.array(int_features)]
    model = joblib.load('models/nslkdd/model_com.sav')
    predict = model.predict(final4)

    if predict==1:
        output='There is No Attack Detected and Its NORMAL!'
    elif predict==0:
        output='Attack is Detected and its DOS Attack!'
    elif predict==2:
        output='Attack is Detected and its PROBE Attack!'
    elif predict==3:
        output='Attack is Detected and its R2L Attack!'
    elif predict==4:
        output='Attack is Detected and its U2R Attack!'
    
    
    return render_template('prediction.html', output=output)


@app.route('/predict1',methods=['POST'])
def predict1():
    int_features= [float(x) for x in request.form.values()]
    print(int_features,len(int_features))
    final4=[np.array(int_features)]
    model = joblib.load('models/kddcup/model_com.sav')
    predict = model.predict(final4)

    if predict==1:
        output='There is No Attack Detected and Its NORMAL!'
    elif predict==0:
        output='Attack is Detected and its DOS Attack!'
    elif predict==2:
        output='Attack is Detected and its PROBE Attack!'
    elif predict==3:
        output='Attack is Detected and its R2L Attack!'
    elif predict==4:
        output='Attack is Detected and its U2R Attack!'
    
    
    return render_template('prediction.html', output=output)


@app.route('/predict2',methods=['POST'])
def predict2():
    int_features= [float(x) for x in request.form.values()]
    print(int_features,len(int_features))
    final4=[np.array(int_features)]
    model = joblib.load('models/cicids2017/model_org.sav')
    predict = model.predict(final4)

    if predict==0:
        output='There is No Attack Detected and Its BENIGN!'
    elif predict==1:
        output='Attack is Detected and its BOT Attack!'
    elif predict==2:
        output='Attack is Detected and its BRUTEFORCE Attack!'
    elif predict==3:
        output='Attack is Detected and its DDOS Attack!'
    elif predict==4:
        output='Attack is Detected and its DOS Attack!'
    elif predict==5:
        output='Attack is Detected and its PORTSCAN Attack!'
    elif predict==6:
        output='Attack is Detected and its WEBATTACK Attack!'
    
    
    return render_template('prediction.html', output=output)

@app.route('/predict3',methods=['POST'])
def predict3():
    int_features= [float(x) for x in request.form.values()]
    print(int_features,len(int_features))
    final4=[np.array(int_features)]
    model = joblib.load('models/cicids2018/model_com.sav')
    predict = model.predict(final4)

    if predict==0:
        output='There is No Attack Detected and Its BENIGN!'
    elif predict==1:
        output='Attack is Detected and its BOT Attack!'
    elif predict==2:
        output='Attack is Detected and its BRUTEFORCE Attack!'
    elif predict==3:
        output='Attack is Detected and its DOS Attack!'
    elif predict==4:
        output='Attack is Detected and its SQL-INJECTION Attack!' 
    
    
    return render_template('prediction.html', output=output)


if __name__ == "__main__":
    app.run(debug=False)

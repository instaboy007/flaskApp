import json
from bson import json_util
from flask import Flask, render_template, request, url_for, redirect,session
from flask_pymongo import PyMongo
import re

app = Flask(__name__)
app.secret_key = "super secret key"
app.config["MONGO_URI"] = "mongodb+srv://instaboy:instaboy@instaboy.hh1km.mongodb.net/userdatabase?retryWrites=true&w=majority&ssl=true&tlsAllowInvalidCertificates=true"
mongo = PyMongo(app)
db = mongo.db.userdata



@app.route('/',methods=('GET','POST'))
@app.route('/index',methods=('GET','POST'))
def index():
    userData=db.find()
    print(userData)
    # userData = [json.dumps(doc, default=json_util.default) for doc in userData]
    #print(userData)
    return render_template('index.html',data=userData)

@app.route('/register', methods=('GET', 'POST'))
def register():
    msg = ''
    print(request)
    if request.method == 'POST' and 'firstName' in request.form and 'lastName' in request.form and 'number[full]' in request.form :
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        fullNumber=request.form['number[full]']
        number = request.form['number[main]']
        if len(firstName)<3:
            msg = 'Atlest 3 Characters requied'
        elif len(lastName)<1:
            msg='Atleast 3 Characters required'
        elif len(number)<10 or len(number)>10:
            msg= 'Invalid Mobile Number'
        elif not firstName or not lastName or not number:
            msg = 'Please fill out the form !'
        else:
            db.insert_one({'firstname':firstName,'lastname':lastName,'number':fullNumber})
            msg = 'You have successfully registered !'
            session['userId']=number
            return redirect(url_for('index'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html',msg=msg)

if __name__=='__main__':
    app.run()


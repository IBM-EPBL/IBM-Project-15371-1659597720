import numpy as np
import cv2
from playsound import playsound
from flask import Flask,request,render_template,redirect,url_for
from cloudant.client import Cloudant
client=Cloudant.iam('1842e7da-7ca7-42f1-8a8e-9d41fd4430b1-bluemix','BwGeC4ciJPGGL2qLxDVa7EOKrSpv7euviPnF76bxeUfO',connect=True)
my_database=client.create_database('my_database')
app=Flask(__name__,template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/index")
def home():
    return render_template("index.html")

@app.route('/result')
def dummy():
    return render_template("result.html")

@app.route('/register')
def reg():
    return render_template("register.html")
@app.route('/afterreg', methods=['POST'])

def afterreg():

    x = [x for x in request.form.values()]

    print(x)
    data = {

    '_id':x[1],

    'name':x[0],

    'psw':x[2]
    }

    print(data)

    query= {'_id': {'$eq': data['_id']}}

    docs = my_database.get_query_result(query)

    print(docs)


    str1 = ""

    # traverse in the string

    print(len(docs.all()))

    if(len(docs.all())==0):
        url=my_database.create_document(data)

    #response requests.get(url)

        return render_template('index.html', pred="Registra")
    else:

        return render_template('register.html', pred="You are")
@app.route('/afterlog',methods=['POST'])
def afterlog():
    user=request.form['email']
    pas=request.form['psw']
    print(user,pas)
    query={'_id':{'$eq':user}}
    docs=my_database.get_query_result(query)
    print(docs)
    print(len(docs.all()))
    if(len(docs.all())==0):
        return render_template('login.html',pred="The username is not found")
    else:
        if((user==docs[0][0]['_id']and pas==docs[0][0]['psw'])):
            print("valid user")
            return render_template('index.html')
        else:
            print('invalid user')
@app.route('/login')
def log():
    return render_template("login.html")
if __name__ == "__main__":
    app.run(debug=True)

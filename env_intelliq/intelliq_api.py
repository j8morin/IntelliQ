#pip install flask
from flask import Flask, render_template, abort, flash, request, redirect, url_for
from werkzeug.exceptions import HTTPException

#pip install flask-wtf
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired, InputRequired
from werkzeug.utils import secure_filename

#pip install flask-sqlalchemy
#from flask_sqlalchemy import SQLAlchemy

#pip install mysql-connector-python
import mysql.connector
from mysql.connector import Error


import json
import os



#-----------------------------------------------------------------------------
#Commande utile dans le powerShell:

#Aciver l'environnement virtuel:
#env_intelliq\Scripts\activate

#set flask app for the environnement: (nécessite surement un redémarrage)
#setx FLASK_APP "api.py"

#Lancer l'application flask:
#flask run
#flask --app api run
#-----------------------------------------------------------------------------

#Connect to database
try:
    connection = mysql.connector.connect(host='localhost',
                                        database='intelliqdb', #j=intelliqdb    r=intelliq_db
                                        user='root',
                                        password='root') #j=root     r=123456
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
except Error as e:
    print("Error while connecting to MySQL", e)

#-----------------------------------------------------------------------------
#Setting up flask app

UPLOAD_FOLDER = 'uploaded_files'
ALLOWED_EXTENSIONS = {'json'}

#Create a Flask instance
app= Flask(__name__)

#Add Secret Key
app.config['SECRET_KEY'] = "123456" 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#app routage
'''def index():
    #abort(500)      #force the error 500
    #raise no_data() #force the error 402
    #raise success() #force the error 200
    return render_template("welcome.html")'''
#-----------------------------------------------------------------------------

#Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What is your username ?", validators=[DataRequired()])
    submit = SubmitField("Submit")
    #Create A String
    def __repr__(self):
        return '<Name %r>' % self.name #show the username, we'll delete this function later

#Create a Surname Page
@app.route('/intelliq_api', methods=['GET', 'POST'])
def user():
    global actualUser
    actualUser = ""
    
    name = None
    form = NamerForm()
    #Validate
    if form.validate_on_submit():
        name = form.name.data
        actualUsername=[name]
        form.name.data = '' #vide zone entrée texte
        #Check if username is already in database
        exist = 0
        cursor.execute("SELECT username,userID FROM users")
        for username in cursor:
            
            if name==username[0] and exist==0:
                flash("This username is already used by someone else")
                exist=1
            else:
                flash("This username is valide")

            
          
        if exist!=1:
            cursor.execute("INSERT INTO users(username) VALUES(%s)",actualUsername)
            connection.commit() #make sure data is committed to the database

        #take the value of userID in function of the usernames
        #cursor.execute("SELECT userID FROM users where username = %s", actualUsername)

        actualUser = actualUsername

    return render_template("login.html",
        name = name,
        form = form)


#---------------------------------------------------------------------------------------------------------------
#route for the healthcheck:
# a JSON object: {"status":"OK", "dbconnection":[connection string]}
# is returned, otherwise {"status":"failed", "dbconnection":[connection string]} is returned. The
# connection string contains the necessary information required for the DB of your choice.
@app.route('/healthcheck')
#Healthcheck
def healthcheck():
    #Connect to database
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='intelliqdb',
                                            user='root',
                                            password='root')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            data = {'status':'OK','dbconnection':db_Info}
            json_data = json.dumps(data)
            cursor = connection.cursor()
            cursor.execute("select database();")
            print(json_data)
    except:
        #print("Error while connecting to MySQL", e)
        db_Info = connection.get_server_info()
        data = {'status':'failed','dbconnection':db_Info}
        json_data=json.dumps(data)
        print(json_data)
    
    #a changer plus tard pour faire apparaitre le json object
    return render_template("healthcheck.html",
        json_data = json_data)
#---------------------------------------------------------------------------------------------------------------
#test
@app.route('/test',methods=['GET', 'POST'])
def test():
    with open('env_intelliq/questionnaire01.json','r') as f:
            questionnaire_data = json.load(f)
        # do something with questionnaire_data
    return render_template("test.html",data = questionnaire_data)

#---------------------------------------------------------------------------------------------------------------
class UploadFileForm(FlaskForm):
    file = FileField("File",validators=[InputRequired()])
    submit = SubmitField("Upload File")

#This function read a questionnaire.json file to add everything to the database
def add_questionnaire_to_db(filename):
    with open(filename,'r') as json_file:
            questionnaire_data = json.load(json_file)
            qID=questionnaire_data['questionnaireID']
            qTitle=questionnaire_data['questionnaireTitle']
            qKeywordsID=questionnaire_data['keywordsID']
            qQuestionsID=questionnaire_data['questionsID']
            print(qID,qTitle)
    if connection.is_connected():
        cursor.execute("INSERT INTO questionnaires(questionnaireID,questionnaireTitle,keywordsID,questionsID) VALUES(%s,%s,%s,%s)",(qID,qTitle,qKeywordsID,qQuestionsID))
        connection.commit() #make sure data is committed to the database

@app.route('/questionnaire_upd',methods=['GET', 'POST'])
def upload_file():
    check=""
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data #Grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) #Save the file
        #Open the file to fill the database
        filename="env_intelliq/uploaded_files/"+file.filename
        add_questionnaire_to_db(filename)
       
        check = "File has been uploaded"
    else:
        check = ""
    return render_template("questionnaire_upd.html",form=form, check=check)


#---------------------------------------------------------------------------------------------------------------
#Create a route 
@app.route('/admin')
def admin():
    if (actualUser[0] == "raphael") or (actualUser[0] == "jules"):
        return render_template("admin.html")
    else:
        abort(401)



#---------------------------------------------------------------------------------------------------------------
#Create Custom Error Pages
#back-end error
@app.errorhandler(500)#: impossible to run with ':'
def internal_server(e):
    return render_template("error_500.html"), 500

#invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error_404.html"), 404

#response is empty
class no_data(HTTPException):
    code = 402
    description = 'response is empty'
def handle_402(e):
    return render_template('error_402.html')
app.register_error_handler(no_data, handle_402)

#request is made by a non-authorized user
@app.errorhandler(401)
def not_authorized(e):
    return render_template("error_401.html"), 401

#parameters given in a call are not valid
@app.errorhandler(400)
def bad_request(e):
    return render_template("error_400.html"), 400

#Successful call returning a non-empty data payload
class success(HTTPException):
    code = 200
    description = 'Successful call returning a non-empty data payload'
def handle_200(e):
    return render_template('error_200.html')
app.register_error_handler(success, handle_200)


#Run port 9103 (port_max=25467)
if __name__ == '__main__':
    app.run(debug=True, port=9103) #need 'pip install cryptography' to use 'ssl_context='adhoc''


#to long to load 
'''
if __name__ == '__main__':
    app.run(debug=True, port=9103, ssl_context='adhoc') #need 'pip install cryptography' to use 'ssl_context='adhoc' <=> https'
    '''
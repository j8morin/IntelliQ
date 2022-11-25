from flask import Flask, render_template, abort
from werkzeug.exceptions import HTTPException

#pip install flask-wtf
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#pip install flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy

#pip install mysql-connector-python
import mysql.connector
from mysql.connector import Error

#-----------------------------------------------------------------------------
#Commande utile dans le powerShell:

#Aciver l'environnement virtuel:
#intelliq\Scripts\activate

#set flask app for the environnement: (nécessite surement un redémarrage)
#setx FLASK_APP "api.py"

#Lancer l'application flask:
#flask run
#flask --app api run
#-----------------------------------------------------------------------------

#import connect to db
try:
    connection = mysql.connector.connect(host='localhost',
                                        database='users_db',
                                        user='root',
                                        password='123456')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
except Error as e:
    print("Error while connecting to MySQL", e)


#Create a Flask instance
app= Flask(__name__)

#Add Secret Key
app.config['SECRET_KEY'] = "123456" 

#Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What is your username ?", validators=[DataRequired()])
    submit = SubmitField("Submit")
    #Create A String
    def __repr__(self):
        return '<Name %r>' % self.name #show the username, we'll delete this function later


#Create a route decorator
#@app.route('/intelliq_api')
'''def index():
    #abort(500)      #force the error 500
    #raise no_data() #force the error 402
    #raise success() #force the error 200
    return render_template("welcome.html")'''


#Create a Surname Page
@app.route('/intelliq_api', methods=['GET', 'POST'])
def user():
    name = None
    form = NamerForm()
    #Validate
    if form.validate_on_submit():
        name = form.name.data
        username=[name]
        form.name.data = '' #vide zone entrée texte
        cursor.execute("INSERT INTO users(username) VALUES(%s)",username)
        
        connection.commit() #make sure data is committed to the database

        cursor.execute("SELECT users.username FROM users") #query operation
        for username in cursor:
            print(username)

    return render_template("login.html",
        name = name,
        form = form)

#Create a route 
@app.route('/admin')
def admin():
    return render_template("admin.html")

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
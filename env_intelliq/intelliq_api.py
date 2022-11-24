from flask import Flask, render_template
#from flask_sqlalchemy import SQLAlchemy

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
a=7+3
c=3
b=5
#Create a Flask instance
app= Flask(__name__)

#Create a route decorator
@app.route('/')

def index():
    return "<h1>Non non Pain<h1>"
# IntelliQ  
IntelliQ project from Software engineering Semester 7 course in Electronical and Computer Engineering School, NTUA.  
Back-end python API and Database model are available on this git.  

### Components
All components can be found in env_intelliq folder:  
- *templates* folder contains all HTML simple templates we created fo every endpoints.  
- *uploaded_files* is the folder where uploaded questionnaires are localy stored.  
- *intelliq_api.py* contains all our python endpoints functions.  
- *QQ000.json* is a questionnaire file who can be used to test the questionnaire upload endpoint.  
- *setup_database.txt* containes all the code you should put in your database QUERY to setup our database model. 

### Authors
- Raphaël Dussauze
- Jules Morin

## Installation

### Python requirements 

The python API needs the following librairy to run:

- flask
- flask-wtf
- mysql-connector-python

You can use the package manager [pip](https://pip.pypa.io/en/stable/) to install these librairy in a python environnement:

```bash
pip install flask
pip install flask-wtf
pip install mysql-connector-python
```

### Database requirements

The test of this API requires a MySQL database that can run on localhost.  
Once your database is created you have to put good connection parameters in *intelliq_api.py API* code part to connect to the database:  
(Line 47)
```bash
connection = mysql.connector.connect(host='localhost',
                                        database='nameOfYourDatabase',
                                        user='YourUserNamer',
                                        password='YourPassword')
```

The healthcheck function also needs your database parameters.

To setup the model we created you just have to copy past and run all the *setup_database.txt* contents in you database Query. (TEST ZONE functions don't need to be run.)

## Usage

Once every all configurations are done and you're SQL database is running, you can run the *intelliq_api.py* 
If everything works fine, your terminal should return this:

```bash
Connected to MySQL Server version  8.0.31
You re connected to database:  ('intelliq_db',)
 * Serving Flask app 'intelliq_api'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on 'http://127.0.0.1:9103'
Press CTRL+C to quit
 * Restarting with stat
Connected to MySQL Server version  8.0.31
You re connected to database:  ('intelliq_db',)
```

The http link is the local host link you should copy past in your browser to test all endpoint.  
You should then enter this link on your browser to start the test:

```bash
http://127.0.0.1:9103/intelliq_api
```

This first page is an identification page.  
To access the admin endpoint you should login as jules or raphael.

To insert a questionnaire in the database, you should use the {baseURL}/admin/questionnaire_upd endpoint and select the *QQ000.json* given questionnaire.





Install Python on your computer 

Add Python to Path
https://stackoverflow.com/questions/65348890/python-was-not-found-run-without-arguments-to-install-from-the-microsoft-store
Environment Variables -> System variables -> Path -> 
D:\Projects\Python312
D:\Projects\Python312\Scripts
close and reopen VSCode

and then attach it with VS Code and create a virtual environment
https://code.visualstudio.com/docs/python/python-tutorial

Extensions view (Ctrl+Shift+X)
Install Python and Python Debugger Extensions

Open the Command Palette (Ctrl+Shift+P), start typing the "Python: Create Environment" command to search, and then select the command.
select Venv
Select the Python interpreter you installed at the beginning of the tutorial.

Open terminal (ctrl+shift+`)
python --version
Install flask - https://code.visualstudio.com/docs/python/tutorial-flask
You can install flask under .venv 
D:\Projects\PythonFlaskVSCodeProject> cd .venv 
D:\Projects\PythonFlaskVSCodeProject\.venv>python -m pip install flask

If you don't do this, flask will be installed directly in parent env that is where the python is installed and that module will be available to all the apps.

create app.py
-------------
    from flask import Flask
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "Hello, Flask!"



To start the server:
    - python -m flask run
    O/P:
    Running on http://127.0.0.1:5000

    - right click in app.py and run as python file
    python app.py
    
    - flask --app app run --debug     ---- somehow this way debugging is not working. 
                                            you have to try below approach
    app.py is consiered as an application here
    As a shortcut, if the file is named app.py or wsgi.py, you don’t have to use --app. 


In Browser,
http://127.0.0.1:5000/


For running in debug mode:
https://code.visualstudio.com/docs/python/tutorial-flask

Switch to the 'Run and Debug' view in VS Code (using the left-side activity bar or Ctrl+Shift+D). 
You may see the message "To customize Run and Debug create a launch.json file". This means that you don't yet have a launch.json file containing debug configurations. 
VS Code can create that for you if you click on the create a launch.json file link:

Scroll down to and examine the configuration, which is named "Python: Flask". 
This configuration contains "module": "flask",, which tells VS Code to run Python with -m flask when it starts the debugger. 
It also defines the FLASK_APP environment variable in the env property to identify the startup file, which is app.py by default, but allows you to easily specify a different file. 
If you want to change the host and/or port, you can use the args array.

launch.json :

{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        

        {
            "name": "Python Debugger: Flask",
            "type": "debugpy",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "app.py",
                "FLASK_DEBUG": "1"
            },
            "args": [
                "run",
                "--no-debugger",
                "--no-reload"
            ],
            "jinja": true,
            "autoStartBrowser": false
        }
    ]
}

Github extension:
https://code.visualstudio.com/docs/sourcecontrol/github
ctrl+shift+x
install the 'GitHub Pull Requests and Issues extension'. 

Jinja2 snippet kit extension:
ctrl+shift+x (open extensions)
Install 'Jinja2 Snippet Kit'


Install sqlalchemy to make flask database work
pip install flask sqlalchemy

Install mysql python connector
pip install mysql-connector-python
pip install mysqlclient 

Flask project youtube video:
https://www.youtube.com/watch?v=oA8brF3w5XQ
Flask application example:
https://www.geeksforgeeks.org/connect-flask-to-a-database-with-flask-sqlalchemy/#creating-apppy
https://flask-sqlalchemy.readthedocs.io/en/stable/queries/
https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/?ref=asr4
https://www.geeksforgeeks.org/flask-url-helper-function-flask-url_for/?ref=asr6

html bootstrap code:
https://getbootstrap.com/docs/5.3/content/tables/

Jinja2 tutorial:
https://documentation.bloomreach.com/engagement/docs/jinja-syntax
https://jinja.palletsprojects.com/en/stable/templates/
it has statements, expressions, comments, filters, tests, control structures

sqlalchemy tutorial:
    SQLAlchemy is the Python SQL toolkit that allows developers to access and manage SQL databases using Pythonic domain language. 
    You can write a query in the form of a string or chain Python objects for similar queries. 

    There are two ways, you can query datbase using SQLAlchemy
    https://www.geeksforgeeks.org/sqlalchemy-tutorial-in-python/
    1. SQLAlchemy Core api
        you can use insert, select etc functions or textual queries
    2. SQLAlchemy ORM api
        creating a Model and querying using that model


    Textual Query api:
    https://www.geeksforgeeks.org/sqlalchemy-tutorial-in-python/
    https://www.datacamp.com/tutorial/sqlalchemy-tutorial-examples


    (ORM)session query api - https://www.geeksforgeeks.org/sqlalchemy-db-session-query/


Flask Session Context
    https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/

g and current_app
    https://flask.palletsprojects.com/en/stable/appcontext/

g:
    https://stackoverflow.com/questions/40881750/whats-the-difference-between-current-app-and-g-context-variable
    g is a special object that is unique for each request. 
    It is used to store data that might be accessed by multiple functions during the request.
    The data stored in g resets after every request.

    https://flask.palletsprojects.com/en/stable/appcontext/
    The g name stands for “global”, but that is referring to the data being global within a context. 
    The data on g is lost after the context ends, and it is not an appropriate place to store data between requests. 
    Use the session or a database to store data across requests.

current_app:
    https://flask.palletsprojects.com/en/stable/appcontext/
    Rather than referring to an app directly, you use the current_app proxy, which points to the application handling the current activity.
    whatever you store in current_app is available app wide till the app is running. 
    It is like an 'application' object in jsp.

    Rather than referring to an app directly, you use the current_app proxy, which points to the application handling the current activity.
    Flask automatically pushes an application context when handling a request. View functions, error handlers, and other functions that run during a request will have access to current_app.
    Flask will also automatically push an app context when running CLI commands registered with Flask.cli using @app.cli.command().

When a request is created, Request Context is pushed by flask. 
A corresponding application context is also pushed when a request context is pushed.
Application context (app_context) is also available when you run the commands from command prompt.

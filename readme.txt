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
    python -m flask run
    O/P:
    Running on http://127.0.0.1:5000


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
install the GitHub Pull Requests and Issues extension. 


Install sqlalchemy to make flask database work
pip install flask sqlalchemy

Install mysql python connector
pip install mysql-connector-python
pip install mysqlclient 

Flask project youtube video:
https://www.youtube.com/watch?v=oA8brF3w5XQ



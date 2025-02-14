from flask import Flask, render_template, request, url_for, redirect
# when I tried to install flask_sqlachemy using pip install flask-sqlalchemy
# it installed in global python library (D:\Projects\Python312\Lib\site-packages) instead of workspace's virtual env(.venv)
# I am not sure why did it do like that
# But now, I have to use global python library as my Python Interpreter instead of venv
# So, ctrl+shift+p, Python: Select Interpreter, choose Global interpreter which is installed at D:\Projects\Python312
# 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re

# initialize an app
app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
# to work with mysql, you need to follow https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://admin:admin@localhost:3306/todo"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ORM in flask
class Todo(db.Model):

    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
       

    def __repr__(self):
        return f"{self.sno} - {self.title}"

# create database
with app.app_context():
    # this will create todo.db and todo table in workspace for sqlite
    # for mysql, you need to have created todo database, this will create todo table in it
    db.create_all()

@app.route("/")
@app.route("/index")
def home():
    #return "Hello, Flask!"
    return render_template("index.html")

@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content


# https://code.visualstudio.com/docs/python/tutorial-flask
# hello_there.html should be in templates folder
@app.route("/hello/")
@app.route("/hello/rendertemplate/<name>")
def hello_there_rendertemplate(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

if __name__=="__main__":
    app.run(debug=True)
    # app.run(debug=True, port=8000)

 

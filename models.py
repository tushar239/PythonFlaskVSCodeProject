
from flask import Flask
# when I tried to install flask_sqlachemy using pip install flask-sqlalchemy
# it installed in global python library (D:\Projects\Python312\Lib\site-packages) instead of workspace's virtual env(.venv)
# I am not sure why did it do like that
# But now, I have to use global python library as my Python Interpreter instead of venv
# So, ctrl+shift+p, Python: Select Interpreter, choose Global interpreter which is installed at D:\Projects\Python312
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# initialize an app
app = Flask(__name__)

# to work with mysql, you need to follow https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application
# DATABASE_URI = "sqlite:///todo.db"
DATABASE_URI = "mysql://admin:admin@localhost:3306/todo"

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
engine = db.create_engine(DATABASE_URI)


# ORM in flask - Declare a mapping
# you need this mapping for ORM api.
# for CORE api, you need to create a table, you don't need this mapping
# https://www.geeksforgeeks.org/sqlalchemy-tutorial-in-python/
class Todo(db.Model):

    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
       
    def __repr__(self):
        return f"{self.sno} - {self.title} - {self.desc}"

# create database
# db instance is available only when app_context is available
# normally, app context is pushed with request context and popped with request context
# It means that app_context will be available when a request is made, but will not be available
# outside the request. If you need it, you have to manually push it using 'with app.app_context()' statement
# Application context (app_context) is also available when you run the commands from command prompt.
# you can run db.create_all from command prompt also.
with app.app_context():
    # this will create todo.db and todo table in workspace for sqlite
    # for mysql, you need to have created todo database, this will create todo table in it
    db.create_all()
    '''
    # somehow, this tries to insert a record twice.
    todo = Todo(title='make money',
               desc='need to take money from the client')

    db.session.add(todo)
    db.session.commit()
    '''
    
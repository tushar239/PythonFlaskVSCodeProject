from flask import Flask
# when I tried to install flask_sqlachemy using pip install flask-sqlalchemy
# it installed in global python library (D:\Projects\Python312\Lib\site-packages) instead of workspace's virtual env(.venv)
# I am not sure why did it do like that
# But now, I have to use global python library as my Python Interpreter instead of venv
# So, ctrl+shift+p, Python: Select Interpreter, choose Global interpreter which is installed at D:\Projects\Python312
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker


# initialize an app
app = Flask(__name__)

# to work with mysql, you need to follow https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application
# DATABASE_URI = "sqlite:///todo.db"
DATABASE_URI = "mysql://admin:admin@localhost:3306/todo"

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
engine = db.create_engine(DATABASE_URI)

# What is session - https://docs.sqlalchemy.org/en/20/orm/session_basics.html
Session = sessionmaker(bind = engine)
session = Session()
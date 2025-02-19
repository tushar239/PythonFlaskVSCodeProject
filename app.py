'''
Flask project youtube video:
https://www.youtube.com/watch?v=oA8brF3w5XQ
Flask application example:
https://www.geeksforgeeks.org/connect-flask-to-a-database-with-flask-sqlalchemy/#creating-apppy
https://flask-sqlalchemy.readthedocs.io/en/stable/queries/
https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/?ref=asr4
https://www.geeksforgeeks.org/flask-url-helper-function-flask-url_for/?ref=asr6
'''

from flask import Flask, render_template, request, url_for, redirect
from sqlalchemy import delete
from sqlalchemy import sql
from sqlalchemy.orm import sessionmaker 
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
        return f"{self.sno} - {self.title}"

# create database
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
    
@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def home_page():
    if request.method == "POST":
        title1 = request.form['title']
        desc1 = request.form['desc']
        #print(title1)
        if title1:
            todo = Todo(title=title1.strip(), desc=desc1.strip())
            db.session.add(todo)
            db.session.commit()
            

    '''
    There are two ways, you can query datbase using SQLAlchemy
    https://www.geeksforgeeks.org/sqlalchemy-tutorial-in-python/
    1. SQLAlchemy Core api
        you can use insert, select etc functions or textual queries
    2. SQLAlchemy ORM api
        creating a Model and querying using that model
    '''

    '''
    # Core api
    sql_query = sql.text("SELECT * FROM todo.todo")
    conn = engine.connect() 
    result_cursor = conn.execute(sql_query) # sqlalchemy.engine.cursor.CursorResult 
    print(result_cursor)
    allTodos = result_cursor.fetchall()
    print(allTodos) # sqlalchemy.engine.result.ScalarResult
    conn.close()
    
    return render_template("index.html", allTodos = allTodos)
    '''

    '''
    # ORM api
    allTodos = Todo.query.all()
    #print(allTodos)
    
    # passing allTodos in variable named allTodos to index.html. 
    # Using Jinja2 templating, I can read this variable in index.html
    return render_template("index.html", allTodos = allTodos) 
    '''

    # ORM api
    #session query api - https://www.geeksforgeeks.org/sqlalchemy-db-session-query/
    Session = sessionmaker(bind=engine) 
    session = Session() 
    allTodos_session_query_api = session.query(Todo).all()
    session.close()
    print(allTodos_session_query_api)
    return render_template("index.html", allTodos = allTodos_session_query_api)

@app.route("/delete/<int:sno>")
def delete_todo(sno):
    #print(sno)
    # from https://www.geeksforgeeks.org/sqlalchemy-orm-query/
    # delete a todo
    Session = sessionmaker(bind=engine) 
    session = Session() 
    # you can use _and, _or in filter query also - https://stackoverflow.com/questions/3332991/sqlalchemy-filter-multiple-columns
    # filter vs filter_by - https://stackoverflow.com/questions/2128505/difference-between-filter-and-filter-by-in-sqlalchemy
    result = session.query(Todo) \
    .filter(Todo.sno == sno) \
    .delete(synchronize_session=False)
    # or
    '''
    result = session.query(Todo) \
    .filter_by(sno = sno) \
    .delete(synchronize_session=False)
    '''

    session.commit()
    print("Rows deleted:", result)
    session.close()
    
    # https://www.geeksforgeeks.org/redirecting-to-url-in-flask/
    # another option is url_for - https://www.geeksforgeeks.org/redirecting-to-url-in-flask/
    return redirect("/")

    '''
    # reload all todos
    Session = sessionmaker(bind=engine)
    session = Session() 
    allTodos = session.query(Todo).all()
    session.close()
    
    return render_template("index.html", allTodos = allTodos)
    '''

@app.route("/updatepage/<int:sno>")
def update_todo_page(sno):
    #print(sno)
    Session = sessionmaker(bind=engine) 
    session = Session() 
    todo = session.query(Todo).filter(Todo.sno == sno).first()
    session.close()
    return render_template("update.html", todo = todo)

@app.route("/update/<int:sno>", methods=['POST'])
def update_todo(sno):
    #print(sno)
    title = request.form['title']
    desc = request.form['desc']
    Session = sessionmaker(bind=engine) 
    session = Session() 
    session.query(Todo)\
        .filter(Todo.sno == sno)\
        .update({Todo.title: title, Todo.desc: desc})
    session.commit()
    session.close()
    
    # reload all todos
    Session = sessionmaker(bind=engine)
    session = Session() 
    allTodos = session.query(Todo).all()
    session.close()
    
    return render_template("index.html", allTodos = allTodos)


@app.route("/show")
def show_todos():
    allTodos = Todo.query.all()
    print(allTodos)
    return str(allTodos)

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
#if __name__=="app":
    app.run(debug=True)
    print("hello")
    # app.run(debug=True, port=8000)
    

 

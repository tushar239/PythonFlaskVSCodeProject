'''
Flask project youtube video:
https://www.youtube.com/watch?v=oA8brF3w5XQ
Flask application example:
https://www.geeksforgeeks.org/connect-flask-to-a-database-with-flask-sqlalchemy/#creating-apppy
https://flask-sqlalchemy.readthedocs.io/en/stable/queries/
https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/?ref=asr4
https://www.geeksforgeeks.org/flask-url-helper-function-flask-url_for/?ref=asr6
'''

from flask import render_template, request, url_for, redirect, g, current_app
from sqlalchemy import delete, update, insert, select
from sqlalchemy import sql
from sqlalchemy.orm import sessionmaker 
import re
from models import app, db, engine, session, Todo, Address, User
from datetime import datetime

#print(__name__)


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def home_page():
    # current_app proxy object refers to current app that is running. you can store data in it which
    # will live till the application is running.
    #current_app.name = 'Tushar';
    #print(current_app.name)
    
    if request.method == "POST":
        title1 = request.form['title']
        desc1 = request.form['desc']
        # g proxy object lives till the request lives. 
        # If you want to share data between different functions within the same request,
        # you can use g proxy.
        #g.title1 = title1
        #g.desc1 = desc1
        
        #print(title1)
        if title1:
            '''
            todo = Todo(title=title1.strip(), desc=desc1.strip())
            db.session.add(todo)
            db.session.commit()
            '''
            # OR
            # https://www.geeksforgeeks.org/sqlalchemy-core-update-statement/
            # Just like update(), you can use insert() also
            stmt = insert(Todo)\
                    .values({"title": title1.strip(), "desc": desc1.strip()})
            db.session.execute(stmt)
            db.session.commit()
            db.session.close()

    '''
    There are two ways, you can query datbase using SQLAlchemy
    https://www.geeksforgeeks.org/sqlalchemy-tutorial-in-python/
    1. SQLAlchemy Core api
        you can use insert, update, select etc functions or textual queries
    2. SQLAlchemy ORM api
        creating a Model and querying using that model
    '''

    '''
    # SQLAlchemy Core Texual SQL api
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
    # SQLAlchemy ORM's Query api
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

    # Just like update(), insert() and delete(), you DON'T have select()
    '''
    stmt = select(Todo)#.where(Todo.title=="read book31")
    allTodos1 = db.session.execute(stmt)
    db.session.close()
    print(allTodos1)
    return render_template("index.html", allTodos = allTodos1)
    '''


@app.route("/delete/<int:sno>")
def delete_todo(sno):
    #print(sno)

 
    # https://www.geeksforgeeks.org/sqlalchemy-core-delete-statement/
    # Just like update() and insert(), you can use delete() also
    stmt = delete(Todo)\
            .where(Todo.sno == sno)
    db.session.execute(stmt)
    db.session.commit()
    db.session.close()

    # OR
    '''
    # from https://www.geeksforgeeks.org/sqlalchemy-orm-query/
    # delete a todo
    Session = sessionmaker(bind=engine) 
    session = Session() 
    # you can use _and, _or in filter query also - https://stackoverflow.com/questions/3332991/sqlalchemy-filter-multiple-columns
    # filter vs filter_by - https://stackoverflow.com/questions/2128505/difference-between-filter-and-filter-by-in-sqlalchemy
    result = session.query(Todo) \
                    .filter(Todo.sno == sno) \
                    .delete(synchronize_session=False)
    
    session.commit()
    print("Rows deleted:", result)
    session.close()
    '''

    # or
    '''
    Session = sessionmaker(bind=engine) 
    session = Session() 

    result = session.query(Todo) \
    .filter_by(sno = sno) \
    .delete(synchronize_session=False)

    session.commit()
    print("Rows deleted:", result)
    session.close()
    '''

    # or
    # you can use a textual query also

    
    # It will find a method with route as '/' and execute it.
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
    # you can use _and, _or in filter query also - https://stackoverflow.com/questions/3332991/sqlalchemy-filter-multiple-columns
    # filter vs filter_by - https://stackoverflow.com/questions/2128505/difference-between-filter-and-filter-by-in-sqlalchemy
    # select * from todo where sno=sno LIMIT 1
    todo = session.query(Todo).filter(Todo.sno == sno).first()
    #print("todo for update: ", todo)
    session.close()
    return render_template("update.html", todo = todo)

@app.route("/update/<int:sno>", methods=['POST'])
def update_todo(sno):
    #print(sno)
    title = request.form['title']
    desc = request.form['desc']
    print(title)

    Session = sessionmaker(bind=engine) 
    session = Session() 
    # https://www.geeksforgeeks.org/sqlalchemy-core-update-statement/
    stmt = update(Todo)\
            .values({"title": title, "desc": desc})\
            .where(Todo.sno == sno)
    session.execute(stmt)
    session.commit()
    session.close()

    # OR
    '''
    Session = sessionmaker(bind=engine) 
    session = Session() 
    # you can use _and, _or in filter query also - https://stackoverflow.com/questions/3332991/sqlalchemy-filter-multiple-columns
    # filter vs filter_by - https://stackoverflow.com/questions/2128505/difference-between-filter-and-filter-by-in-sqlalchemy
    # select * from todo where sno=sno LIMIT 1
    todo = session.query(Todo).filter(Todo.sno == sno).first()
    todo.title = title
    todo.desc = desc
    session.add(todo)
    session.close()
    '''
    
    # OR
    '''
    Session = sessionmaker(bind=engine) 
    session = Session() 
    session.query(Todo)\
        .filter(Todo.sno == sno)\
        .update({Todo.title: title, Todo.desc: desc})
    session.commit()
    session.close()
    '''
    
    # OR
    '''
    # SQLAlchemy Core Texual SQL api
    sql_query = sql.text("update todo.todo t set t.title="+"'"+title+"'"+","+"t.desc="+"'"+desc+"'"+" where t.sno="+str(sno))
    #sql_query = sql.text("update todo.todo as t set t.title="+title+","+"t.desc="+desc+" where t.sno="+str(sno))
    conn = engine.connect() 
    result_cursor = conn.execute(sql_query) # sqlalchemy.engine.cursor.CursorResult 
    conn.commit()
    conn.close()
    '''

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


@app.route("/create_user")
def create_user():
    user1 = User(name="John Doe", age=52)
    user2 = User(name="John Smith", age=34)

    address1 = Address(city="New York", state="NY", zip_code="1001")
    address2 = Address(city="New Jersey", state="NJ", zip_code="2001")
    address3 = Address(city="Chicago", state="IL", zip_code="3001")

    user1.addresses.extend([address1, address2])
    user2.addresses.append(address3)

    session.add(user1)
    session.add(user2)
    session.commit()

    print(f"<address1's user={address1.user}>")
    print(f"<address2's user={address2.user}>")
    print(f"<address3's user={address3.user}>")
    #print(f"<user1's addresses={user1.addresses}>")
    #print(f"<user2's addresses={user2.addresses}>")

    return "Users created. Check DB."

@app.route("/get_user/<id>")
def getUser(id):
    Session = sessionmaker(bind=engine) 
    session = Session() 
    # you can use _and, _or in filter query also - https://stackoverflow.com/questions/3332991/sqlalchemy-filter-multiple-columns
    # filter vs filter_by - https://stackoverflow.com/questions/2128505/difference-between-filter-and-filter-by-in-sqlalchemy
    # select * from users where id=id LIMIT 1
    user = session.query(User).filter(User.id == id).first()
    
    print("User: ", user)
    print("User's addresses: ", user.addresses)
    ret = "User: "+ str(user) +"\n" + "Addresses: " + str(user.addresses)
    #ret = "User: "+ str(user)

    session.close()
    
    #print(ret)
    return ret

@app.route("/get_address/<id>")
def getAddress(id):
    Session = sessionmaker(bind=engine) 
    session = Session() 
    # you can use _and, _or in filter query also - https://stackoverflow.com/questions/3332991/sqlalchemy-filter-multiple-columns
    # filter vs filter_by - https://stackoverflow.com/questions/2128505/difference-between-filter-and-filter-by-in-sqlalchemy
    # select * from addresses where id=id LIMIT 1
    address = session.query(Address).filter(Address.id == id).first()
    
    print("Address: ", address)
    print("Address's User: ", address.user)
    ret = "Address: "+ str(address) +"\n" + "User: " + str(address.user)
    #ret = "Address: "+ str(address)

    session.close()

    #print(ret)
    return ret

if __name__=="__main__":
#if __name__=="app":
    app.run(debug=True)
    print("hello")
    # app.run(debug=True, port=8000)
    

 


from init_database import app, db, engine, session
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime



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

#########################################################################################3

'''
one-to-many relationship
https://www.youtube.com/watch?v=3N9JqtpkFJI
'''

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    __allow_unmapped__ = True

    id = db.Column(db.Integer, primary_key = True)

class Address(BaseModel):
    __tablename__ = "addresses" # name of the table in database

    city = Column(String(200))
    state = Column(String(200))
    zip_code = Column(String(20))
    user_id = Column(ForeignKey("users.id"))

    def __repr__(self):
        return f"<Address(id={self.id}, city={self.city})>"

class User(BaseModel):
    __tablename__ = "users"

    name = Column(String(200))
    age = Column(Integer)
    addresses = relationship(Address) # user can have list of addresses. When you Basesave user, you can save addresses also with it
    
    def __repr__(self):
            return f"<User(id={self.id}, name={self.name})>"


Base.metadata.create_all(engine)




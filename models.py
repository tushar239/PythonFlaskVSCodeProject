
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
https://thegirlsynth.hashnode.dev/mastering-sqlalchemy-relationships-exploring-the-backpopulates-parameter-and-different-relationship-types

back_populates property = https://stackoverflow.com/questions/39869793/when-do-i-need-to-use-sqlalchemy-back-populates
Back-populates is used in conjunction with the relationship() function in SQLAlchemy. 
It is defined on both sides of the relationship and allows for automatic population of related objects. 
This means that when one object is updated, its related objects are automatically updated as well.

Without back_populates, it gives following warning.
SAWarning: relationship 'User.addresses' will copy column users.id to column addresses.user_id, which conflicts with relationship(s): 'Address.user' (copies users.id to addresses.user_id). 
If this is not the intention, consider if these relationships should be linked with back_populates, or if viewonly=True should be applied to one or more if they are read-only. 
For the less common case that foreign key constraints are partially overlapping, the orm.foreign() annotation can be used to isolate the columns that should be written towards.   
To silence this warning, add the parameter 'overlaps="user"' to the 'User.addresses' relationship. (Background on this warning at: https://sqlalche.me/e/20/qzyx) (This warning originated from the `configure_mappers()` process, which was invoked automatically in response to a user-initiated operation.)
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
    user = relationship("User", back_populates="addresses") 

    def __repr__(self):
        return f"<Address(id={self.id}, city={self.city})>"
    '''
    def __str__(self):
        return f"<Address(id={self.id}, city={self.city})>, user={self.user}"
    '''

class User(BaseModel):
    __tablename__ = "users"

    name = Column(String(200))
    age = Column(Integer)
    # user object can have list of address object. 
    # When you save/retrieve user, you can save/retrieve addresses also with it
    addresses = relationship("Address", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, name={self.name})>"
    '''
    def __str__(self):
        return f"<User(id={self.id}, name={self.name}), addresses={self.addresses}>"
    '''

Base.metadata.create_all(engine)




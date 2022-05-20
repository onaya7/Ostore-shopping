from enum import unique
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_login import UserMixin



db=SQLAlchemy()



#Models

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email =db.Column(db.String(100), unique =True)
    password = db.Column(db.String(100))


def __repr__(self):
        return f'<Admin {self.id}>'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Product(UserMixin, db.Model):

    __tablename__='product'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64), unique=True)
    price = db.Column(db.Float, nullable=False)
    filename = db.Column(db.String(64), unique=True, nullable=False,)

    def __repr__(self):
        return '<Product> %r' % self.id


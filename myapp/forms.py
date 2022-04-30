from wsgiref.validate import validator
from flask_wtf import Form
from wtforms import (StringField, TextAreaField, IntegerField, PasswordField, BooleanField, RadioField, validators)




class Signup(Form):
    email = StringField('Email Address',[validators.Length(min=4, max=25)])
    name = StringField('Name',[validators.Length(min=6, max=35)])
    password= PasswordField('New Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

class Login(Form):
    email = StringField('Email Address',[validators.Length(min=4, max=25)])
    password= PasswordField('New Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
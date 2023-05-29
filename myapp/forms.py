from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email,EqualTo,ValidationError, Regexp
from myapp.models import User


class RegistrationForm(FlaskForm):
    firstname = StringField('First name*', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('last Name*', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(
        min=6, max=35, message='Little short for an email address?')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password'), Length(min=5, max=50, message="Password is too short"), Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$',message='Password must include at least one uppercase letter, one lowercase letter, one number, and one special character')])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email is taken. Please choose a different one")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(
        min=6, max=35)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign in')


class UpdateAccountForm(FlaskForm):
    firstname = StringField('First Name',validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')


    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('that email is taken. please choose a different one.')

class EmailForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')



class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password'), Length(min=5, max=50, message="Password is too short"), Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$',message='Password must include at least one uppercase letter, one lowercase letter, one number, and one special character')])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Submit')
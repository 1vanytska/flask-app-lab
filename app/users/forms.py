from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from app.users.models import User
from wtforms import ValidationError

def email_exists(form, field):
    user = User.query.filter_by(email=field.data).first()
    if user:
        raise ValidationError('Email is already registered.')

def username_exists(form, field):
    user = User.query.filter_by(username=field.data).first()
    if user:
        raise ValidationError('Username is already taken.')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=3, max=20), 
        Regexp('^[A-Za-z][A-Za-z0-9_]*$', 
               message = 'Username must start with a letter and contain only letters, numbers, and underscores'),
        username_exists
    ])
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(), 
        email_exists
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=6, max=60)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password')
    ])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')

from flask_wtf import FlaskForm
from wtforms import BooleanField, FileField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from app.users.models import User
from wtforms import ValidationError
from flask_login import current_user
from flask_wtf.file import FileAllowed

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

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20), Regexp('^[A-Za-z][A-Za-z0-9_]*$', message="Username must start with a letter and contain only letters, numbers, and underscores")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])  # Додаємо поле для зображень
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is already taken.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is already registered.')

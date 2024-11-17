from flask import session
from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, SelectField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField("Title", 
                        validators=[DataRequired(), Length(min=2, max=10)])
    content = TextAreaField("Content", validators=[DataRequired()])
    publication_date = DateField('Publish Date',
                                 format='%Y-%m-%d', validators=[DataRequired()])
    category = SelectField('Category', choices=[('tech', 'Tech'), ('science', 'Science'), ('lifestyle', 'Lifestyle')], validators=[DataRequired()])
    is_active = BooleanField('Is not Active', default=False)
    author = StringField("Author", validators=[DataRequired(), Length(min=2, max=10)])
    submit = SubmitField("Add Post")
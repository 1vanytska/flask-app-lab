from flask import session
from flask_wtf import FlaskForm
from wtforms import BooleanField, DateTimeLocalField, SelectField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField("Title", 
                        validators=[DataRequired(), Length(min=2, max=10)])
    content = TextAreaField("Content", validators=[DataRequired()])
    publish_date = DateTimeLocalField('Publish Date',
                                      format='%Y-%m-%dT%H:%M',  # ISO формат для дати й часу
                                      validators=[DataRequired()])
    category = SelectField('Category', choices=[('tech', 'Tech'), ('science', 'Science'), ('lifestyle', 'Lifestyle')], validators=[DataRequired()])
    is_active = BooleanField('NOT Active', default=True)
    submit = SubmitField("Add Post")
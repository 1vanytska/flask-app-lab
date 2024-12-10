from datetime import datetime as dt
from flask import session
from flask_wtf import FlaskForm
from wtforms import BooleanField, DateTimeLocalField, SelectField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField("Title", 
                        validators=[DataRequired(), Length(min=2, max=10)])
    content = TextAreaField("Content", validators=[DataRequired()])
    publish_date = DateTimeLocalField('Publish Date',
                                      format='%Y-%m-%dT%H:%M',
                                      default=dt.now(),
                                      validators=[DataRequired()])
    category = SelectField('Category', choices=[('tech', 'Tech'), ('science', 'Science'), ('lifestyle', 'Lifestyle')], validators=[DataRequired()])
    is_active = BooleanField('Active', default=True)
    author_id = SelectField("Author", coerce=int)

    submit = SubmitField("Add Post")
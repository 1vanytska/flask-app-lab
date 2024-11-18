from flask import session
from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, SelectField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField("Title", 
                        validators=[DataRequired(), Length(min=2, max=10)])
    content = TextAreaField("Content", validators=[DataRequired()])
    publish_date  = DateField('Publish Date',
                                 format='%Y-%m-%d', validators=[DataRequired()])
    category = SelectField('Category', choices=[('tech', 'Tech'), ('science', 'Science'), ('lifestyle', 'Lifestyle')], validators=[DataRequired()])
    is_active = BooleanField('NOT Active', default=True)
    submit = SubmitField("Add Post")
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, FloatField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from app.orders.models import Category

class CreateOrderForm(FlaskForm):
    name = StringField(
        'Order Name',
        validators=[DataRequired(), Length(max=100)]
    )
    comment = StringField(
        'Comment',
        validators=[Length(max=255)]
    )
    price = FloatField(
        'Price',
        validators=[DataRequired(), NumberRange(min=0.0, message="Price must be non-negative")]
    )
    categories = SelectMultipleField(
        'Categories',
        choices=[],
        coerce=int
    )
    submit = SubmitField('Create Order')

class SearchForm(FlaskForm):
    search_field = StringField('Search', validators=[DataRequired()])
    search_by = SelectField('Search by', choices=[
        ('name', 'Name'),
        ('comment', 'Comment'),
        ('price', 'Price')
    ], validators=[DataRequired()])
    category_id = SelectField('Category', choices=[
        (category.id, category.name) for category in Category.query.all()
    ])
    ignore_category_filter = SelectField('Ignore Category', choices=[
        ('yes', 'Yes'), 
        ('no', 'No')
    ], default='no')
    sort_by = SelectField('Sort by', choices=[
        ('name', 'Name'),
        ('price', 'Price')
    ], validators=[DataRequired()])
    submit = SubmitField('Search')
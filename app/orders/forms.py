from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

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

from . import order_bp
from flask import render_template, redirect, url_for, flash
from app import db
from app.orders.models import Order, Category
from .forms import CreateOrderForm, SearchForm

@order_bp.route('/orders', methods=['GET', 'POST'])
def orders():
    form = SearchForm()

    orders_query = Order.query

    if form.ignore_category_filter.data == 'no' and form.category_id.data:
        orders_query = orders_query.join(Order.categories).filter(Category.id == form.category_id.data)

    if form.search_field.data:
        search_field = form.search_by.data
        search_value = form.search_field.data
        orders_query = orders_query.filter(getattr(Order, search_field).like(f'%{search_value}%'))

    sort_by = form.sort_by.data
    orders_query = orders_query.order_by(getattr(Order, sort_by))

    orders = orders_query.all()

    return render_template('orders.html', form=form, orders=orders)

@order_bp.route('/create_order', methods=['GET', 'POST'])
def create_order():
    form = CreateOrderForm()
    
    form.categories.choices = [(category.id, category.name) for category in Category.query.all()]
    
    if form.validate_on_submit():
        order = Order(
            name=form.name.data,
            comment=form.comment.data,
            price=form.price.data,
        )
        selected_categories = Category.query.filter(Category.id.in_(form.categories.data)).all()
        order.categories.extend(selected_categories)

        db.session.add(order)
        db.session.commit()
        flash('Order created successfully!', 'success')
        return redirect(url_for('.orders'))
    
    return render_template('create_order.html', form=form)

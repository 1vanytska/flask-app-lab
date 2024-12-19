from . import order_bp
from flask import render_template, redirect, url_for, flash
from app import db
from app.orders.models import Order, Category
from .forms import CreateOrderForm

@order_bp.route('/orders', methods=['GET'])
def orders():
    all_orders = Order.query.all()
    return render_template('orders.html', orders=all_orders)

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

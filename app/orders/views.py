from . import order_bp
from flask import render_template, redirect, url_for, flash
from app import db
from app.orders.models import Order, Category
from .forms import CreateOrderForm, SearchForm, EditOrderForm 

@order_bp.route('/<int:order_id>', methods=['GET'])
def order_details(order_id):
    order = Order.query.get_or_404(order_id)

    return render_template('order_details.html', order=order)

@order_bp.route('/edit/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    order = Order.query.get_or_404(order_id)
    form = EditOrderForm(obj=order)

    form.categories.choices = [(category.id, category.name) for category in Category.query.all()]
    
    selected_categories = [category.id for category in order.categories]
    form.categories.data = selected_categories
    
    if form.validate_on_submit():
        order.name = form.name.data
        order.comment = form.comment.data
        order.price = form.price.data
        order.categories = Category.query.filter(Category.id.in_(form.categories.data)).all()
        
        db.session.commit()
        flash('Order updated successfully!', 'success')
        return redirect(url_for('orders.order_details', order_id=order.id))
    
    return render_template('edit_order.html', form=form, order=order)


@order_bp.route('/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    
    flash('Order deleted successfully!', 'danger')
    return redirect(url_for('orders.orders_list'))


@order_bp.route('/orders', methods=['GET', 'POST'])
def orders_list():
    form = SearchForm()

    orders_query = Order.query

    if form.ignore_category_filter.data == 'no' and form.category_id.data:
        orders_query = orders_query.join(Order.categories).filter(Category.id == form.category_id.data)

    if form.search_field.data:
        search_field = form.search_by.data
        search_value = form.search_field.data
        orders_query = orders_query.filter(getattr(Order, search_field).like(f'%{search_value}%'))

    sort_by = form.sort_by.data
    if sort_by:
        orders_query = orders_query.order_by(getattr(Order, sort_by))

    orders = orders_query.all()

    return render_template('orders_list.html', form=form, orders=orders)


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
        return redirect(url_for('.orders_list'))
    
    return render_template('create_order.html', form=form)

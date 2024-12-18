from app import db

order_category = db.Table('order_category',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)

    categories = db.relationship('Category', secondary=order_category, back_populates='orders')

    def __repr__(self):
        return f"<Order {self.name} - {self.price} USD>"

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    orders = db.relationship('Order', secondary=order_category, back_populates='categories')

    def __repr__(self):
        return f"<Category {self.name}>"

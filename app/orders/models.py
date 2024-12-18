from app import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Назва замовлення
    comment = db.Column(db.Text, nullable=True)       # Коментар до замовлення
    price = db.Column(db.Float, nullable=False)       # Ціна замовлення
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    def __repr__(self):
        return f"<Order {self.name} - {self.price}>"
    
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)                # Ім'я клієнта
    email = db.Column(db.String(120), unique=True, nullable=False)  # Електронна пошта клієнта
    about_customer = db.Column(db.Text, nullable=True)              # Додаткова інформація про клієнта

    orders = db.relationship('Order', backref='customer', lazy=True)

    def __repr__(self):
        return f"<Customer {self.name} - {self.email}>"


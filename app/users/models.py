from app import db, bcrypt, login_manager
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=True, default='default.jpg')
    about_me = db.Column(db.String(200), nullable=True, default="")
    last_seen = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"User('{self.email}')"

    def hash_password(self, password):
        return bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def update_last_seen(self):
        self.last_seen = datetime.utcnow()
        db.session.commit()
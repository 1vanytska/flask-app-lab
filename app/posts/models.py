from app import db
from datetime import datetime as dt

class Post(db.Model):
    __tablename__='posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    publish_date = db.Column(db.DateTime, nullable=False)
    # author = db.Column(db.String(120), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    author = db.relationship('User', backref="posts", lazy="select")

    def __repr__(self):
        return f"<Post(title={self.title}, category={self.category}, author={self.author})>"
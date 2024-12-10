from sqlalchemy.orm import backref
from app import db
from datetime import datetime as dt

post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

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
    author = db.relationship('User', backref=backref("posts", lazy="dynamic"), lazy="joined")
    tags = db.relationship('Tag', secondary=post_tags, back_populates='posts')

    def __repr__(self):
        return f"<Post(title={self.title}, category={self.category}, author={self.author})>"
    
class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    # Зв'язок "багато до багатьох" з постами
    posts = db.relationship('Post', secondary=post_tags, back_populates='tags')
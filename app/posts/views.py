from . import post_bp
from app import db
from flask import render_template, abort, flash, session, url_for, redirect, request
from app.users.models import User
from app.posts.models import Post
from .forms import PostForm
from .utils import load_posts, save_post, get_post


@post_bp.route('/add_post', methods=["GET", "POST"]) 
def add_post():
    
    form = PostForm()

    authors = User.query.all()
    form.author_id.choices = [(author.id, author.username) for author in authors]

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        category = form.category.data
        is_active = form.is_active.data
        publish_date  = form.publish_date.data
        author = session.get('username', 'Anonymous')
        
        new_post = Post(
            title = title,
            content = content,
            category = category,
            is_active = is_active,
            publish_date = publish_date,
            author = author
        )
        
        db.session.add(new_post)
        db.session.commit()
        flash(f"Post {title} added successfully!", "success")
        return redirect(url_for(".get_posts"))
    elif request.method == "POST":
        flash(f"Enter the correct data in the form!", "danger")
        
    return render_template("add_post.html", form=form)

@post_bp.route('/') 
def get_posts():
    posts = Post.query.order_by(Post.publish_date.desc()).all()
    return render_template("posts.html", posts=posts)

@post_bp.route('/<int:id>') 
def detail_post(id):
    post = Post.query.get_or_404(id)
    return render_template("detail_post.html", post=post)

@post_bp.route('/delete', methods=['POST'])
def delete_post():
    post_id = request.form.get('post_id')
    post = Post.query.get(post_id)
    if not post:
        flash("Post not found!", "error")
        return redirect(url_for('.get_posts'))

    db.session.delete(post)
    db.session.commit()

    flash("Post deleted successfully!", "success")
    return redirect(url_for('.get_posts'))

@post_bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = db.get_or_404(Post, post_id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.is_active.data
        post.publish_date = form.publish_date.data
        db.session.commit()
        flash('Post updated successfully!', "success")
        return redirect(url_for('.detail_post', id=post.id))
    return render_template('add_post.html', form=form)

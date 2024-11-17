from . import post_bp
from flask import render_template, abort, flash, session, url_for, redirect, request
from .forms import PostForm
from .utils import load_posts, save_post, get_post


@post_bp.route('/add_post', methods=["GET", "POST"]) 
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        title=form.title.data,
        content=form.content.data,
        category=form.category.data,
        is_active=form.is_active.data,
        author=session.get('username', 'Anonymous')
        
        new_post = {'id': len(load_posts()) + 1, 
                    'title': title, 'content': content, 
                    'category': category,
                    'is_active': is_active,
                    'author': author,
        }

        save_post(new_post)
        flash(f"Post {title} added successfully!", "success")
        return redirect(url_for(".get_posts"))
    elif request.method == "POST":
        flash(f"Enter the correct data in the form!", "danger")
        
    return render_template("add_post.html", form=form)

@post_bp.route('/') 
def get_posts():
    posts = load_posts()
    return render_template("posts.html", posts=posts)

@post_bp.route('/<int:id>') 
def detail_post(id):
    post = get_post(id)
    if not post:
        return abort(404)
    return render_template("detail_post.html", post=post)
    
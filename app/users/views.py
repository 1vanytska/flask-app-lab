import os
import uuid
from . import user_bp
from flask import current_app, flash, make_response, redirect, render_template, request, session, url_for
from app import db
from app.users.models import User
from .forms import RegistrationForm, LoginForm
from datetime import datetime, timedelta
from flask_login import login_user, logout_user, current_user, login_required
from .forms import UpdateAccountForm
from werkzeug.utils import secure_filename
from .forms import ChangePasswordForm

@user_bp.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            hashed_password = current_user.hash_password(form.new_password.data)
            current_user.password = hashed_password
            
            db.session.commit()

        flash("Your password has been updated!", "success")
        return redirect(url_for('users.login'))

    return render_template('change_password.html', form=form)

@user_bp.route("/edit_profile", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html', form=form)

def save_picture(form_picture):
    if form_picture:
        random_hex = uuid.uuid4().hex
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(current_app.root_path, 'users/static/profile_image', picture_fn)
        
        form_picture.save(picture_path)
        return picture_fn
    else:
        return None

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = User().hash_password(form.password.data)
        user = User(username=form.username.data, 
                    email=form.email.data, 
                    password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash('Your account has been created!', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)

@user_bp.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=form.remember.data)
            user.last_seen = datetime.now()
            db.session.commit()
            flash('Successfully logged in!', 'success')
            return redirect(url_for('users.account'))
        flash("Invalid username or password.", "danger")
    return render_template("login.html", form=form)

@user_bp.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    current_user.last_seen = datetime.now()
    db.session.commit()
    return render_template('account.html', user=current_user)

@user_bp.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("Successfully logged out.", "success")
    return redirect(url_for('users.login'))

@user_bp.route("/users", methods=['GET'])
@login_required
def all_users():
    users = User.query.all()
    return render_template('all_users.html', users=users)

VALID_USERNAME = "user"
VALID_PASSWORD = "123"

@user_bp.route("/profile")
def get_profile():
    if "username" in session:
        username_value = session["username"]
        cookies = request.cookies
        theme = request.cookies.get('theme', 'light')
        return render_template("profile.html", cookies=cookies, username=username_value, theme=theme)
    flash("You need to log in to access this page.", "danger")
    return redirect(url_for("users.login"))

@user_bp.route('/profile/add_cookie', methods=['POST'], endpoint='profile_add_cookie')
def profile_add_cookie():
    key = request.form['key']
    value = request.form['value']
    duration = request.form.get('duration', 3600)

    response = make_response(redirect(url_for('users.get_profile')))
    response.set_cookie(key, value, max_age=int(duration))
    flash(f"Cookie '{key}' added successfully!", "success")
    return response


@user_bp.route('/profile/delete_cookie', methods=['POST'], endpoint='profile_delete_cookie')
def profile_delete_cookie():
    key = request.form['key']
    response = make_response(redirect(url_for('users.get_profile')))
    response.delete_cookie(key)
    flash(f"Cookie '{key}' deleted successfully!", "warning")
    return response


@user_bp.route('/profile/delete_all_cookies', methods=['POST'], endpoint='profile_delete_all_cookies')
def profile_delete_all_cookies():
    response = make_response(redirect(url_for('users.get_profile')))
    for key in request.cookies.keys():
        response.delete_cookie(key)
    flash("All cookies deleted successfully!", "danger")
    return response

@user_bp.route('/set_theme/<theme>')
def set_theme(theme):
    if theme in ['light', 'dark']:
        response = make_response(redirect(url_for('users.get_profile')))
        response.set_cookie('theme', theme, max_age=60 * 60 * 24 * 30)  # 30 days
        return response
    flash("Invalid theme selected.", "danger")
    return redirect(url_for('users.get_profile'))

@user_bp.route('/hi/<string:name>') # --> user/hi/sofiia?age=19
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, type = int)
    return render_template("users/hi.html", name=name, age=age)

@user_bp.route('/admin')
def admin():
    to_url = url_for("users.greetings", name="administrator", _external=True)    # --> "http://localhost:8080/user/hi/administrator"
    print(to_url)
    return redirect(to_url)

@user_bp.route('/set_cookie')
def set_cookie():
    response = make_response('Кука встановлена')
    response.set_cookie('username', 'student', max_age=timedelta(minutes=5))
    response.set_cookie('color', '', max_age=timedelta(minutes=5))
    return response

@user_bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    return request.cookies

@user_bp.route('/delete_cookie')
def delete_cookie():
    response = make_response('Кука видалена')
    response.set_cookie('username', '', expires=0) # response.set_cookie('username', '', max_age=0)
    return response

@user_bp.route('/homepage')
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return render_template("home.html", agent=agent)

@user_bp.route('/resume')
def resume():
    return render_template('resume.html', title='Sofiia Ivanytska - Resume')
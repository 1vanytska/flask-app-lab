from . import user_bp
from flask import flash, make_response, redirect, render_template, request, session, url_for
from app import db
from app.users.models import User
from .forms import RegistrationForm
from datetime import datetime, timedelta

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
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session["username"] = user.username
            session.permanent = True
            flash("Successfully logged in!", "success")
            return redirect(url_for("users.account"))
        else:
            flash("Invalid username or password.", "danger")
            return redirect(url_for("users.login"))
    
    return render_template("login.html")

@user_bp.route("/account")
def account():
    username = session.get("username")
    if not username:
        flash("You must be logged in to view your profile", "danger")
        return redirect(url_for("users.login"))
    
    user = User.query.filter_by(username=username).first()
    return render_template("account.html", user=user)

@user_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash("Successfully logged out.", "info")
    return redirect(url_for('users.login'))

@user_bp.route('/users')
def users():
    users_list = User.query.all()
    
    if not users_list:
        return render_template('users.html', message="There are no registered users.")
    
    return render_template('users.html', users=users_list, count=len(users_list))

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


# @user_bp.route("/login", methods=['GET', 'POST'])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
        
#         if username == VALID_USERNAME and password == VALID_PASSWORD:
#             session["username"] = username
#             session.permanent = True
#             flash("Successfully logged in!", "success")
#             return redirect(url_for("users.get_profile"))
#         else:
#             flash("Invalid username or password.", "danger")
#             return redirect(url_for("users.login"))
#     return render_template("login.html")

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


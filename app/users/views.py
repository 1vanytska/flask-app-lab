from . import user_bp
from flask import make_response, redirect, render_template, request, url_for
from datetime import datetime, timedelta

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
    response.set_cookie('username', 'student', max_age=timedelta(seconds=60))
    response.set_cookie('color', '', max_age=timedelta(seconds=60))
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
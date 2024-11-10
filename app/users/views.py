from . import user_bp
from flask import redirect, render_template, abort, request, url_for

@user_bp.route('/hi/<string:name>') # --> user/hi/sofiia?age=19
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, type = int)
    return render_template("hi.html", name=name, age=age)

@user_bp.route('/admin')
def admin():
    to_url = url_for("users.greetings", name="administrator", _external=True)    # --> "http://localhost:8080/user/hi/administrator"
    print(to_url)
    return redirect(to_url)
from flask import abort, request, redirect, url_for, render_template
from . import app

@app.route('/')
def main():
    return render_template('base.html')

@app.route('/homepage')
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return render_template("home.html", agent=agent)

# users

@app.route('/hi/<string:name>') # hi\sofiia?age=19
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, type = int)
    return render_template("hi.html", name=name, age=age)

@app.route('/admin')
def admin():
    to_url = url_for("greetings", name="administrator", _external=True)    # --> "http://localhost:8080/hi/administrator"
    print(to_url)
    return redirect(to_url)

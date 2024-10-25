from flask import Flask, request, redirect, url_for
app = Flask(__name__)    

@app.route('/')   # URL '/' to be handled by main() route handler
def main():
    return 'Hello, world!'

@app.route('/homepage')
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return f"<h1>This is your Home page :) - {agent}</h1>"

@app.route('/hi/<string:name>') # hi\sofiia?age=19
def greetings(name):
    name = name.upper()
    age = request.args.get("age", 0, type = int)
    return f"Welcome {name=} {age=}", 200

@app.route('/admin')
def admin():
    to_url = url_for("greetings", name="administrator", _external=True)               # --> "hi/administrator"
    print(to_url)
    return redirect(to_url)

def home():
    """View for the Home page of your website."""
    return "<h1>This is your Home page :)</h1>"

if __name__ == "__main__":
    app.run()  # Launch built-in web server and run this Flask webapp, debug=True
 


from flask import Flask  # From module flask import class Flask
app = Flask(__name__)    # Construct an instance of Flask class for our webapp

@app.route('/')          # URL '/' to be handled by main() route handler
def main():
    return 'Hello, world!'

if __name__ == '__main__':
    app.run(debug=True)  # Launch built-in web server and run this Flask webapp

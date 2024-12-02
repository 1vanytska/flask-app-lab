from datetime import timedelta

SECRET_KEY = "secret"
FLASK_DEBUG = 1
PERMANENT_SESSION_LIFETIME = timedelta(seconds=60)

SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False
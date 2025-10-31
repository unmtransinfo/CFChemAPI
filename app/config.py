# config.py
from os import environ

# FLASK_ENV not used in newer versions of FLASK, but in this project this var is used to update paths
# according to whether or not we are in a prod environment
FLASK_ENV = environ.get("FLASK_ENV")

# App
APP_NAME = environ.get("APP_NAME")
APP_PORT = environ.get("APP_PORT")
APP_URL = environ.get("APP_URL") or "localhost"
URL_PREFIX = environ.get("URL_PREFIX") or ""

# Database
DB_HOST = environ.get("DB_HOST")
DB_DATABASE = environ.get("DB_DATABASE")
DB_USER = environ.get("DB_USER")
DB_PASSWORD = environ.get("DB_PASSWORD")
DB_PORT = environ.get("DB_PORT")

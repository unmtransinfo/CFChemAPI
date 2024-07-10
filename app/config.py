# config.py
from os import environ

# App
APP_NAME = environ.get("APP_NAME")
APP_PORT = environ.get("APP_PORT")
APP_URL = environ.get("APP_URL") or "localhost"

from blueprints.version import register_routes
from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    # Load config
    load_dotenv(".env")
    app.config.from_pyfile("config.py")
    # Register routes
    VERSION_URL_PREFIX = f"/api/v1"
    CORS(app)
    swagger = Swagger(app)
    register_routes(app, VERSION_URL_PREFIX)
    return app


app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config.get("APP_PORT"))

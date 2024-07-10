from blueprints.version import version
from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
# Load config
load_dotenv(".env")
app.config.from_pyfile("config.py")
# Register routes
app.register_blueprint(version)
CORS(app)
swagger = Swagger(app)

# Main loop
if __name__ == "__main__":
    print(app.url_map)
    app.run(host="0.0.0.0", port=app.config.get("APP_PORT"), debug=True)

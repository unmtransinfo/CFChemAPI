from flask import Flask, Blueprint, jsonify
from blueprints.lincs import lincs
from database.database import database
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv('.env')
app.config.from_pyfile('config.py')
# Set the route prefix based on version
version = Blueprint('/api/v1', __name__, url_prefix="/api/v1")

# Test Route
@version.route('/')
def hello():
	return f'{app.config.get("APP_NAME")} : Hello World!'

# Register routes
version.register_blueprint(lincs)
app.register_blueprint(version)

# Main loop
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=app.config.get('APP_PORT'))
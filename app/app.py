from flask import Flask, Blueprint, jsonify
from database.database import database
from blueprints.version import version
from flasgger import Swagger
from flask_cors import CORS

from dotenv import load_dotenv

app = Flask(__name__)
# Load config
load_dotenv('.env')
app.config.from_pyfile('config.py')
# Register routes
app.register_blueprint(version)
CORS(app)
swagger = Swagger(app)

# Main loop
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=app.config.get('APP_PORT'))
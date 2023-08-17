from flask import Flask, Blueprint, jsonify
from database.database import database
from blueprints.version import version
from marshmallow import Schema, fields
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from dotenv import load_dotenv

app = Flask(__name__)
# Load config
load_dotenv('.env')
app.config.from_pyfile('config.py')

# Auto-Generate Swagger Docs
class DefaultParameter(Schema):
    gist_id = fields.Int()


class DefaultSchema(Schema):
    id = fields.Int()
    content = fields.Str()
spec = APISpec(
    title=app.config.get('APP_NAME'),
    version="1.0.0",
    openapi_version="3.0.2",
    doc='/docs',
    info=dict(
        description=app.config.get('APP_NAME'),
        version="1.0.0-oas3",
        contact=dict(
            email="test@example.com"
            ), 
        license=dict(
            name="Apache 2.0",
            url='http://www.apache.org/licenses/LICENSE-2.0.html'
            )
        ),
    servers=[
        dict(
            description="Test server",
            url="https://resources.donofden.com"
            )
        ],
    tags=[
        dict(
            name="Demo",
            description="Endpoints related to Demo"
            )
        ],
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

spec.components.schema("Default", schema=DefaultSchema)



# Register routes
app.register_blueprint(version)

# Main loop
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=app.config.get('APP_PORT'))
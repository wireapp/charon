import logging
import sys
from importlib import util as importing

from flask import Flask
from flask_restx import Api

from roman.RomanAPI import roman_api
from services.VersionApi import version_api
from slack.SlackAPI import slack_api

# Create app
app = Flask(__name__)

# Set up Swagger and API
authorizations = {
    'bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(app, authorizations=authorizations)

# Register namespaces
api.add_namespace(roman_api, path='/roman')
api.add_namespace(slack_api, path='/slack')
api.add_namespace(version_api, path='/version')

# Load configuration
config_file = 'config'
if importing.find_spec(config_file):
    app.config.from_object(config_file)

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] - %(levelname)s - %(module)s: %(message)s',
                    stream=sys.stdout)
logger = logging.getLogger(__name__)

# App startup
if __name__ == '__main__':
    logger.info('Starting the application.')
    app.run(host="localhost", port=8080)

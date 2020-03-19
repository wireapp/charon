import logging
from importlib import util as importing

from flask import Flask

from roman.RomanAPI import roman_api
from services.TokenDatabase import BotRegistration
from slack.SlackAPI import slack_api

# Create app
app = Flask(__name__)

app.register_blueprint(roman_api, url_prefix='/roman')
app.register_blueprint(slack_api, url_prefix='/slack')

# Load configuration
config_file = 'config'
if importing.find_spec(config_file):
    app.config.from_object(config_file)

BotRegistration.load_from_env()

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] - %(levelname)s - %(module)s: %(message)s')
logger = logging.getLogger(__name__)

# App startup
if __name__ == '__main__':
    logger.info('Starting the application.')
    app.run(host="localhost", port=8080)

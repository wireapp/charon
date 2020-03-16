import dataclasses
from importlib import util as importing

from flask import Flask, jsonify

from common.Utils import get_configuration
from roman.RomanAPI import roman_api
from services.TokenDatabase import BotRegistration
from slack.SlackAPI import slack_api

app = Flask(__name__)

app.register_blueprint(roman_api, url_prefix='/roman')
app.register_blueprint(slack_api, url_prefix='/slack')

config_file = 'config'

if importing.find_spec(config_file):
    app.config.from_object(config_file)

BotRegistration.load_from_env()


@app.route('/')
def hello_world():
    return jsonify(dataclasses.asdict(get_configuration()))


if __name__ == '__main__':
    app.run(host='localhost', port=8080)

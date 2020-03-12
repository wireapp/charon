import dataclasses

from flask import Flask, jsonify

from common.Utils import get_configuration
from roman.RomanAPI import roman_api
from slack.SlackAPI import slack_api

app = Flask(__name__)

app.register_blueprint(roman_api, url_prefix='/roman')
app.register_blueprint(slack_api, url_prefix='/slack')

app.config.from_object('config')


@app.route('/')
def hello_world():
    return jsonify(dataclasses.asdict(get_configuration()))


if __name__ == '__main__':
    app.run(host='localhost', port=8080)

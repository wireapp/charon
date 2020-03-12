from flask import Flask

from roman.RomanAPI import roman_api
from slack.SlackAPI import slack_api

app = Flask(__name__)

app.register_blueprint(roman_api, url_prefix='/roman')
app.register_blueprint(slack_api, url_prefix='/slack')


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

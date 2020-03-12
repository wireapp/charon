from flask import Blueprint

slack_api = Blueprint('slack_api', __name__)


@slack_api.route('/messages')
def messages():
    return 'Slack API'

from flask import Blueprint, jsonify, request

slack_api = Blueprint('slack_api', __name__)


@slack_api.route('/messages', methods=['POST'])
def messages():
    json = request.get_json()
    print(type(json))
    print(json)
    return {'name': 'Slack API'}


@slack_api.route('/messages2')
def messages2():
    return jsonify({'name': 'Slack API'})

from flask import Blueprint, jsonify, request

slack_api = Blueprint('slack_api', __name__)


@slack_api.route('/chat.postMessage', methods=['POST'])
def messages():
    json = request.get_json()
    print(type(json))
    print(json)
    return {'name': 'Slack API'}


@slack_api.route('/messages2')
def messages2():
    return jsonify({'name': 'Slack API'})

# a = {'headers': {'User-Agent': 'Python/3.7.6 slackclient/2.5.0 Darwin/19.3.0', 'Content-Type':
# 'application/json;charset=utf-8', 'Authorization': 'Bearer
# xoxb-997934200070-982943897618-Zodk8bP4tZJ4RKZp3EsWoWok'}, 'data': None, 'files': None, 'params': None,
# 'json': {'ts': '', 'username': 'pythonboardingbot', 'icon_emoji': ':robot_face:', 'blocks': [{'type': 'section',
# 'text': {'type': 'mrkdwn', 'text': "Welcome to Slack! :wave: We're so glad you're here. :blush:\n\n*Get started by
# completing the steps below:*"}}], 'channel': 'DUZK3KTC1'}, 'ssl': None, 'proxy': None, 'auth': None}

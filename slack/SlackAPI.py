import logging

from flask import Blueprint, request, jsonify

from common.Utils import get_configuration, generate_timestamp
from slack.converter.MessageConverter import NewMessage

slack_api = Blueprint('slack_api', __name__)


@slack_api.route('/chat.postMessage', methods=['POST'])
def messages():
    config = get_configuration()

    json = request.get_json()

    logging.info(f'New message received: {json}')
    bearer_token = request.headers['Authorization'].split("Bearer ", 1)[1]

    logging.info('Bearer found.')
    message_id = NewMessage(config).process_bot_message(bearer_token, json)
    logging.info(f'Message sent with id: {message_id}')
    # TODO determine corect response
    return jsonify({'ok': True, 'channel': json['channel'], 'ts': generate_timestamp()})

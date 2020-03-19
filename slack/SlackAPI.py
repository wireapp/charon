import logging

from flask import Blueprint, request, jsonify

from common.Utils import get_configuration, generate_timestamp
from slack.converter.MessageConverter import NewMessage

slack_api = Blueprint('slack_api', __name__)

logger = logging.getLogger(__name__)


@slack_api.route('/chat.postMessage', methods=['POST'])
def messages():
    logger.info('New message from bot received.')
    json = request.get_json()

    logger.debug(f'Message payload: {json}')
    logger.debug(f'Message headers: {request.headers}')

    bearer_token = request.headers['Authorization'].split("Bearer ", 1)[1]

    logger.info('Request authorized')
    config = get_configuration()

    logger.info('Processing the message.')
    message_id = NewMessage(config).process_bot_message(bearer_token, json)
    logger.info(f'Message sent with id: {message_id}')
    return jsonify({'ok': True, 'channel': json['channel'], 'ts': generate_timestamp()})

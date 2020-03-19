import logging

from flask import Blueprint, request, jsonify

from common.Utils import generate_timestamp, auth_denied
from services.Repository import get_conversation_checked
from slack.MessagesHandler import handle

slack_api = Blueprint('slack_api', __name__)

logger = logging.getLogger(__name__)


@slack_api.route('/chat.postMessage', methods=['POST'])
def messages():
    logger.info('New message from bot received.')

    json = request.get_json()
    logger.debug(f'Message payload: {json}')
    logger.debug(f'Message headers: {request.headers}')

    try:
        bot_id = json['channel']
        bearer_token = request.headers['Authorization'].split("Bearer ", 1)[1]
        conversation = get_conversation_checked(bot_id=bot_id, used_api_key=bearer_token)
        if not conversation:
            return auth_denied()
    except Exception:
        logger.exception('Exception during auth.')
        return auth_denied()

    logger.info('Request authorized, handling message.')
    handle(conversation, json)

    return jsonify({'ok': True, 'channel': bot_id, 'ts': generate_timestamp()})

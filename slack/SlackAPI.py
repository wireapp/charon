import logging

from flask import request, jsonify
from flask_restx import Namespace, fields, Resource

from common.Utils import generate_timestamp, auth_denied
from services.Repository import get_conversation_checked
from slack.MessagesHandler import handle

logger = logging.getLogger(__name__)

slack_api = Namespace('slack', description='API exposed for the Slack Bots.')


@slack_api.route('/chat.postMessage', methods=['POST'])
class Messages(Resource):
    dummy_model = slack_api.model('Message', {
        'channel': fields.String(required=True, description='Channel to which is the request sent.')
    })

    @slack_api.doc(
        security='bearer',
        body=dummy_model
    )
    def post(self):
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


# this inspection is not working properly for the classes
# noinspection PyUnresolvedReferences
@slack_api.route('/webhook/<string:api_key>/<string:bot_id>', methods=['POST'])
class Webhooks(Resource):
    dummy_model = slack_api.model('Message', {
        'channel': fields.String(required=True, description='Channel to which is the request sent.')
    })

    @slack_api.doc(
        body=dummy_model,
        params={
            'api_key': 'API key used in the bot registration process.',
            'bot_id': 'Id of the bot in the conversation.'
        }
    )
    def post(self, api_key, bot_id):
        logger.info(api_key)
        logger.info(bot_id)
        logger.info('New message from bot received.')

        json = request.get_json()

        conversation = get_conversation_checked(bot_id=bot_id, used_api_key=api_key)
        if not conversation:
            return auth_denied()

        logger.info('Request authorized, handling message.')
        handle(conversation, json)

        return jsonify({'ok': True, 'channel': bot_id, 'ts': generate_timestamp()})

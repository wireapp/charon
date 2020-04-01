import logging
import uuid

from dacite import from_dict
from flask import request, jsonify, Response
from flask_restx import Namespace, fields, Resource

from common.SlackBot import TwoWayBot, Bot
from common.Utils import auth_denied
from roman.TypeHandler import handle
from services.Repository import register_bot

logger = logging.getLogger(__name__)

roman_api = Namespace('roman', description='API exposed for the Roman.')


@roman_api.route('/messages', methods=['POST'])
class MessagesApi(Resource):
    dummy_model = roman_api.model('Message', {
        'type': fields.String(required=True, description='Type of the message.')
    })

    @roman_api.doc(
        security='bearer',
        body=dummy_model
    )
    def post(self):
        logger.info('Incoming message')

        json = request.get_json()

        try:
            logger.info(f'Obtaining bearer')
            bearer_token = request.headers['Authorization'].split("Bearer ", 1)[1]
            logger.debug('Bearer exist')
        except KeyError:
            logger.warning(f'Bearer token could not be obtained')
            return auth_denied()

        handle(json, bearer_token)

        return jsonify({'success': True})


@roman_api.route('/registration', methods=['POST'])
class RegisterBot(Resource):
    bot_registration = roman_api.model('BotRegistration', {
        'bot_token': fields.String(required=True, description='Token sent with every request to Slack Bot.'),
        'signing_secret': fields.String(required=True,
                                        description='Secret which is used for signing every request body sent to bot.'),
        'bot_api_key': fields.String(required=True,
                                     description='Slack Bot\'s API key used for accessing Slack and Charon.'),
        'bot_url': fields.String(required=True, description='URL of the bot, where it is running.'),
        'authentication_code': fields.String(required=True,
                                             description='Authentication code used by Roman to verify it\'s requests.')
    })

    @roman_api.doc(
        body=bot_registration,
        validate=True
    )
    def post(self):
        logger.info('Registering new bot.')

        json = request.get_json()
        try:
            logger.debug(json)
            bot = from_dict(data_class=TwoWayBot, data=json)
            token = json['authentication_code']
        except Exception:
            logger.exception('Unexpected or missing data.')
            return Response('Unexpected or missing data.', 400)

        register_bot(token, bot)
        logger.info(f'Bot with id {bot.bot_api_key} registered.')
        return jsonify({'success': True})


@roman_api.route('/registration/hook', methods=['POST'])
class RegisterHookOnlyBot(Resource):
    bot_registration = roman_api.model('WebHookOnlyBot', {
        'bot_api_key': fields.String(required=False,
                                     description='Slack Bot\'s API key used for accessing Slack and Charon. '
                                                 'In case that this bot uses webhook only API, it can be empty.'),
        'authentication_code': fields.String(required=True,
                                             description='Authentication code used by Roman to verify it\'s requests.'),
    })

    @roman_api.doc(
        body=bot_registration,
        validate=True
    )
    def post(self):
        logger.info('Registering new bot.')

        json = request.get_json()
        try:
            logger.info(json)

            token = json['authentication_code']
            bot_api_key = json.get('bot_api_key')

            # validate that api key is set
            if not bot_api_key:
                logger.info('No API key provided, generating new.')
                bot_api_key = str(uuid.uuid4())
        except Exception:
            logger.exception('Unexpected or missing data.')
            return Response('Unexpected or missing data.', 400)

        register_bot(token, Bot(bot_api_key))
        logger.info(f'Bot with id {bot_api_key} registered.')
        return jsonify({'success': True})

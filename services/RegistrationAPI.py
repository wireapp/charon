import logging
import uuid

from dacite import from_dict
from flask import request, jsonify, Response
from flask_restx import Namespace, fields, Resource

from common.SlackBot import TwoWayBot, Bot
from services.Repository import register_bot

logger = logging.getLogger(__name__)

registration_api = Namespace('registration', description='API used for bot registration.')


@registration_api.route('', methods=['POST'])
class RegisterBot(Resource):
    bot_registration = registration_api.model('BotRegistration', {
        'bot_token': fields.String(required=True, description='Token sent with every request to Slack Bot.'),
        'signing_secret': fields.String(required=True,
                                        description='Secret which is used for signing every request body sent to bot.'),
        'bot_api_key': fields.String(required=True,
                                     description='Slack Bot\'s API key used for accessing Slack and Charon.'),
        'bot_url': fields.String(required=True, description='URL of the bot, where it is running.'),
        'authentication_code': fields.String(required=True,
                                             description='Authentication code used by Roman to verify it\'s requests.')
    })

    @registration_api.doc(
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


@registration_api.route('/hook', methods=['POST'])
class RegisterHookOnlyBot(Resource):
    bot_registration = registration_api.model('WebHookOnlyBot', {
        'bot_api_key': fields.String(required=False,
                                     description='Slack Bot\'s API key used for accessing Slack and Charon. '
                                                 'If this value is empty, random API key is generated.'),
        'authentication_code': fields.String(required=True,
                                             description='Authentication code used by Roman to verify it\'s requests.'),
    })

    @registration_api.doc(
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

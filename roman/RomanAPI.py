import logging

from dacite import from_dict
from flask import request, jsonify, Response
from flask_restx import Namespace, fields, Resource

from common.SlackBot import BotRegistration
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
            logger.info(json)
            bot = from_dict(data_class=BotRegistration, data=json)
            token = json['authentication_code']
        except Exception:
            logger.exception('Unexpected or missing data.')
            return Response('Unexpected or missing data.', 400)

        register_bot(token, bot)
        logger.info(f'Bot with id {bot.bot_api_key} registered.')
        return jsonify({'success': True})


@roman_api.route('/status')
class Status(Resource):
    status = roman_api.model('ServiceStatus', {
        'status': fields.String(required=True, description='Indication of service\'s health.', enum=['OK', 'Failing'])
    })

    @roman_api.marshal_with(status)
    def status(self):
        """
        Service API for the ingress
        """
        logger.debug('Stats call - ok')
        return jsonify({'status': 'OK'})

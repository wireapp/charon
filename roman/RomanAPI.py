import logging

from dacite import from_dict, Config as DaciteConf
from flask import Blueprint, request, jsonify, Response

from common.SlackBot import BotRegistration
from common.Utils import auth_denied
from roman.TypeHandler import handle
from services.Repository import register_bot

roman_api = Blueprint('roman_api', __name__)
logger = logging.getLogger(__name__)


@roman_api.route('/messages', methods=['POST'])
def messages_api():
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
def bot_registration():
    logger.info('Registering new bot.')

    json = request.get_json()
    try:
        bot = from_dict(data_class=BotRegistration, data=json, config=DaciteConf(strict=False))
        token = json['authentication_code']
    except Exception:
        return Response('Unexpected or missing data.', 400)

    register_bot(token, bot)
    logger.info(f'Bot with id {bot.bot_api_key} registered.')
    return jsonify({'success': True})


@roman_api.route('/status')
def status():
    """
    Service API for the ingress
    """
    logger.debug('Stats call - ok')
    return jsonify({'success': True})

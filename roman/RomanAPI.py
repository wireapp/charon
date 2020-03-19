import logging

from flask import Blueprint, request, jsonify, Response

from common.Config import get_config
from common.SlackBot import SlackBot
from roman.TypeHandler import handle
from services.TokenDatabase import BotRegistration

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
        logger.error(f'Bearer token could not be obtained')
        return Response('Bearer token not found.', 401)

    config = get_config()
    handle(config, json, bearer_token)

    return jsonify({'success': True})


@roman_api.route('/status')
def status():
    """
    Service API for the ingress
    """
    logger.debug('Stats call - ok')
    return jsonify({'success': True})


@roman_api.route('/registration', methods=['POST'])
def register_bot():
    r = request.get_json()
    logger.info('Registering new bot.')

    BotRegistration.add_bot(SlackBot(
        id=r['id'],
        url=r['url'],
        signing_secret=r['signing_secret'],
        to_proxy_token=r['proxy_token'],
        to_bot_token=r['bot_token']
    ))
    logger.info(f'Bot with id {r["id"]} registered.')
    return jsonify({'success': True})

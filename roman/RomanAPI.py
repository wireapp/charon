from threading import Thread

from flask import Blueprint, request, jsonify

from common.Config import SlackBot
from common.Utils import get_configuration
from roman.TypeHandler import handle
from services.TokenDatabase import BotRegistration

roman_api = Blueprint('roman_api', __name__)


@roman_api.route('/', methods=['POST'])
@roman_api.route('/messages', methods=['POST'])
def messages_api():
    # TODO verify that this is the way
    config = get_configuration()
    Thread(target=handle, args=(config, request.get_json(),)).start()
    return jsonify({'success': True})


@roman_api.route('/registration', methods=['POST'])
def register_bot():
    r = request.get_json()

    BotRegistration.add_bot(SlackBot(
        id=r['id'],
        url=r['url'],
        signing_secret=r['signing_secret'],
        to_proxy_token=r['proxy_token'],
        to_bot_token=r['bot_token']
    ))
    return jsonify({'success': True})

from threading import Thread

from flask import Blueprint, request, jsonify

from common.Utils import get_configuration
from roman.TypeHandler import handle

roman_api = Blueprint('roman_api', __name__)


@roman_api.route('/', methods=['POST'])
@roman_api.route('/messages', methods=['POST'])
def messages_api():
    # TODO verify that this is the way
    config = get_configuration()
    Thread(target=handle, args=(config, request.get_json(),)).start()
    return jsonify({'success': True})

import json
from threading import Thread

from flask import Blueprint, request

from roman.TypeHandler import handle

roman_api = Blueprint('roman_api', __name__)


@roman_api.route('/messages', methods=['POST'])
def messages_api():
    # TODO verify that this is the way

    Thread(target=handle, args=request.get_json()).start()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

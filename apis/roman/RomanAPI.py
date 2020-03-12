from flask import Blueprint

roman_api = Blueprint('roman_api', __name__)


@roman_api.route('/messages')
def accountList():
    return 'Roman API'

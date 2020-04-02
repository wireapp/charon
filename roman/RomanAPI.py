import logging

from flask import request, jsonify
from flask_restx import Namespace, fields, Resource

from common.Utils import auth_denied
from roman.TypeHandler import handle

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
        logger.info('Incoming message from Roman')

        json = request.get_json()

        try:
            logger.debug(f'Obtaining bearer')
            bearer_token = request.headers['Authorization'].split("Bearer ", 1)[1]
            logger.debug('Bearer exist')
        except KeyError:
            logger.warning(f'Bearer token could not be obtained.')
            logger.debug(f'Exception during request: header: {request.headers} payload: {json}')
            return auth_denied()

        handle(json, bearer_token)

        return jsonify({'success': True})

import logging

from flask import jsonify
from flask_restx import Namespace, Resource, fields

from common.Version import get_version

logger = logging.getLogger(__name__)

charon_api = Namespace('charon', description='Service API for running Charon.')


@charon_api.route('/version', methods=['GET'])
class Messages(Resource):
    version_model = charon_api.model('Message', {
        'version': fields.String(required=True, description='Version of running code.')
    })

    @charon_api.response(code=200, model=version_model, description="Returns version of the code")
    def get(self):
        return jsonify({'version': get_version()})

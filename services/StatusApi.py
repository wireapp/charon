from flask import jsonify
from flask_restx import Namespace, Resource, fields

status_api = Namespace('service')


@status_api.route('status', methods=['GET'])
class Status(Resource):
    status = status_api.model('ServiceStatus', {
        'status': fields.String(required=True, description='Indication of service\'s health.', enum=['OK', 'Failing'])
    })

    @status_api.response(code=200, model=status, description="Returns ok if service is healthy.")
    def get(self):
        return jsonify({'status': 'OK'})

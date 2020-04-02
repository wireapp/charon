import logging
import os

from flask import jsonify, g, current_app as app
from flask_restx import Namespace, Resource, fields

logger = logging.getLogger(__name__)

version_api = Namespace('service')


@version_api.route('version', methods=['GET'])
class Version(Resource):
    version_model = version_api.model('Version', {
        'version': fields.String(required=True, description='Version of running code.')
    })

    @version_api.response(code=200, model=version_model, description="Returns version of the code")
    def get(self):
        return jsonify({'version': get_version()})


def get_version() -> str:
    """
    Retrieves version from the flask app.
    """
    if 'version' not in g:
        g.version = read_version('development')

    return g.version


def read_version(default: str) -> str:
    """
    Reads version from the file or returns default version.
    """
    file_path = os.environ.get('RELEASE_FILE_PATH')
    file_path = file_path if file_path else app.config.get('RELEASE_FILE_PATH')
    logger.debug(f'File path: {file_path}')

    version = None
    if file_path:
        with open(file_path, 'r') as file:
            version = file.readline().strip()
            logger.info(f'Settings version as: {version}')

    return version if version else default

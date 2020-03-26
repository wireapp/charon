import logging
import os

from flask import current_app as app

from common.Utils import get_or_set

logger = logging.getLogger(__name__)


def get_version() -> str:
    """
    Retrieves version from the charon.
    """
    return get_or_set('version', lambda: read_version('default'))


def read_version(default: str) -> str:
    """
    Reads version from the file or returns default version.
    """
    file_path = os.environ.get('RELEASE_FILE_PATH')
    file_path = file_path if file_path else app.config.get('RELEASE_FILE_PATH')
    logger.info(f'File path: {file_path}')
    if file_path:
        with open(file_path, 'r') as file:
            version = file.readline().strip()
            logger.info(f'Settings version as: {version}')

    return version if version else default

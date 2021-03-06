import logging
import os
from dataclasses import dataclass
from typing import Optional

from flask import current_app as app

from common.Utils import get_or_set

logger = logging.getLogger(__name__)


@dataclass
class Config:
    """
    Where is the Roman running.
    """
    roman_url: str

    """
    Redis configuration
    """
    redis_url: str
    redis_port: int
    redis_username: Optional[str]
    redis_password: Optional[str]

    """
    URL of the Charon - to generate webhook links correctly
    """
    charon_url: str


def get_config() -> Config:
    """
    Obtains configuration from the application context.
    """
    return get_or_set('config', build_configuration)


def build_configuration() -> Config:
    """
    Builds configuration from environment or from the Flask properties
    """
    logger.debug('Building configuration.')
    config = Config(roman_url=sanitize_url(get_prop('ROMAN_URL')),
                    redis_url=get_prop('REDIS_URL'),
                    redis_port=int(get_prop('REDIS_PORT')),
                    redis_username=get_prop('REDIS_USERNAME', True),
                    redis_password=get_prop('REDIS_PASSWORD', True),
                    charon_url=sanitize_url(get_prop('CHARON_URL')))
    logger.debug(f'Used configuration: {config}')
    return config


def sanitize_url(url: str, protocol: str = 'https://') -> str:
    """
    Takes URL, removes last / and prepends protocol.

    >>> sanitize_url('charon.com/something/')
    'https://charon.com/something'
    """
    sanitized = url[0:-1] if url[-1] == '/' else url
    with_protocol = sanitized if sanitized.startswith('http') else f'{protocol}{sanitized}'
    return with_protocol


def get_prop(name: str, optional: bool = False) -> str:
    """
    Gets property from environment or from the flask env.
    """
    config = os.environ.get(name, app.config.get(name))
    if not optional and not config:
        logger.error(f'It was not possible to retrieve configuration for property "{name}"!')
        raise EnvironmentError(f'No existing configuration for "{name}" found!')
    return config

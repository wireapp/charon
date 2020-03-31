import os
from dataclasses import dataclass

from flask import current_app as app

from common.Utils import get_or_set


@dataclass
class Config:
    roman_url: str

    redis_url: str
    redis_port: int

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
    return Config(roman_url=get_prop('ROMAN_URL'), redis_url=get_prop('REDIS_URL'),
                  redis_port=int(get_prop('REDIS_PORT')),
                  charon_url=get_prop('CHARON_URL'))


def get_prop(name: str) -> str:
    """
    Gets property from environment or from the flask env.
    """
    env = os.environ.get(name)
    return env if env else app.config[name]

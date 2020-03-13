import time

from flask import current_app as app

from common.Config import Config


def generate_timestamp() -> int:
    return int(time.time())


def get_configuration() -> Config:
    return Config(roman_url=app.config['ROMAN_URL'])

import time

from flask import current_app as app

from common.Config import Config


def generate_timestamp() -> int:
    return int(time.time())


def get_configuration() -> Config:
    config = app.config['CHARON_CONFIG']
    return Config(roman_url=config['ROMAN_URL'], signing_secret=config['SIGN_SECRET'], bot_url=config['BOT_URL'])

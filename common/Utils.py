import os
import time

from flask import current_app as app

from common.Config import Config


def generate_timestamp() -> int:
    return int(time.time())


def get_configuration() -> Config:
    roman_url = os.environ.get('ROMAN_URL')
    return Config(roman_url=roman_url if roman_url else app.config['ROMAN_URL'])

import logging
import os
import sys
import time

from flask import current_app as app

from common.Config import Config


def logger(name):
    root = logging.getLogger(name)
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    return root


def generate_timestamp() -> int:
    return int(time.time())


def get_configuration() -> Config:
    roman_url = os.environ.get('ROMAN_URL')
    return Config(roman_url=roman_url if roman_url else app.config['ROMAN_URL'])

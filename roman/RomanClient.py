import logging
from typing import Callable

import requests

from common.Config import Config

logger = logging.getLogger(__name__)


class RomanClient:
    def __init__(self, config: Config):
        self.url = config.roman_url

    def send_text_message(self, token: str, payload: str) -> dict:
        return self.send_message(token, {'type': 'text', 'text': {'data': payload}})

    def send_message(self, token: str, payload: dict) -> dict:
        logger.info(f'Sending message to roman.')
        logger.debug(f'Message payload: {payload}')

        return self.__send(
            lambda: requests.post(f"{self.url}/conversation", json=payload,
                                  headers={"Authorization": f"Bearer {token}"}))

    def get_conversation_info(self, token: str) -> dict:
        logger.info('Obtaining conversation info.')
        return self.__send(
            lambda: requests.get(f"{self.url}/conversation", headers={"Authorization": f"Bearer {token}"}))

    @staticmethod
    def __send(call: Callable) -> dict:
        r = call()
        json = r.json()
        if r:
            logger.debug(f'Request successful. Payload: {json}')
        else:
            logger.warning(f'Roman responded with error! Status {r.status_code}, payload: {json}')
            raise Exception('It was not possible to contact roman!')
        return json

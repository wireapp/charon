import logging

import requests

from common.Config import Config

logger = logging.getLogger(__name__)


class RomanClient:
    def __init__(self, config: Config):
        self.url = config.roman_url

    def send_text_message(self, token: str, payload: str) -> str:
        return self.send_message(token, {'type': 'text', 'text': {'data': payload}})

    def send_message(self, token: str, payload: dict) -> str:
        logger.info(f'Sending message to roman.')
        logger.debug(f'Message payload: {payload}')

        r = requests.post(f"{self.url}/conversation", json=payload, headers={"Authorization": f"Bearer {token}"})

        logger.info('Message sent')
        json = r.json()
        logger.debug(f'Roman response: {json}')
        return json

    def get_conversation_info(self, token: str) -> dict:
        logger.info('Obtaining conversation info')
        r = requests.get(f"{self.url}/conversation", headers={"Authorization": f"Bearer {token}"})
        return r.json()

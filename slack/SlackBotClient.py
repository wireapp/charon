import json
import logging

import requests

from common.SlackBot import TwoWayBot
from common.Utils import generate_timestamp
from slack.SigningService import SigningService

logger = logging.getLogger(__name__)


class SlackBotClient:
    def __init__(self, bot: TwoWayBot):
        self.signing = SigningService(bot.signing_secret)
        self.url = bot.bot_url

    def send(self, payload: dict):
        data = json.dumps(payload)
        logger.debug(f'Sending payload: {payload}')

        headers = self.__prepare_header(generate_timestamp(), data)
        logger.debug(f'With headers: {headers}')

        response = requests.post(self.url, data=data, headers=headers)
        logger.debug(f'Response: {response}')

    def __prepare_header(self, timestamp: int, payload: str) -> dict:
        bytes_payload = payload.encode('utf-8')
        signature = self.signing.generate_signature(timestamp, bytes_payload)
        return {
            'Content-Type': 'application/json',
            'X-Slack-Request-Timestamp': str(timestamp),
            'X-Slack-Signature': signature
        }

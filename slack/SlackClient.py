import json
import time

import requests

from common.Config import Config
from slack.SigningService import SigningService


class SlackClient:
    def __init__(self, config: Config):
        self.signing_secret = config.signing_secret
        self.url = config.bot_url

    def send(self, payload: dict):
        data = json.dumps(payload)
        timestamp = int(time.time())
        headers = self.__prepare_header(timestamp, data)

        response = requests.post(self.url, data=data, headers=headers)
        # TODO find what is response

    def __prepare_header(self, timestamp: int, payload: str) -> dict:
        bytes_payload = payload.encode('utf-8')
        signature = SigningService(self.signing_secret).generate_signature(timestamp, bytes_payload)
        return {
            'Content-Type': 'application/json',
            'X-Slack-Request-Timestamp': timestamp,
            'X-Slack-Signature': signature
        }

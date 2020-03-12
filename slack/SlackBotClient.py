import json

import requests

from common.Config import Config
from common.Utils import generate_timestamp
from slack.SigningService import SigningService


class SlackBotClient:
    def __init__(self, config: Config):
        self.signing_secret = config.signing_secret
        self.url = config.bot_url

    def send(self, payload: dict):
        data = json.dumps(payload)
        headers = self.__prepare_header(generate_timestamp(), data)

        response = requests.post(self.url, data=data, headers=headers)
        print(response)  # TODO find what is response

    def __prepare_header(self, timestamp: int, payload: str) -> dict:
        bytes_payload = payload.encode('utf-8')
        signature = SigningService(self.signing_secret).generate_signature(timestamp, bytes_payload)
        return {
            'Content-Type': 'application/json',
            'X-Slack-Request-Timestamp': str(timestamp),
            'X-Slack-Signature': signature
        }

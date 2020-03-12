import json

import requests

from common.Config import Config


class RomanClient:
    def __init__(self, config: Config):
        self.url = config.roman_url

    def send_message(self, token: str, payload: dict) -> str:
        r = requests.post(f"{self.url}/conversation", data=json.dumps(payload),
                          headers={"content-type": "application/json", "Authorization": f"Bearer {token}"})
        return r.json()['messageId']

    def get_conversation_info(self, token: str) -> dict:
        r = requests.get(f"{self.url}/conversation", headers={"Authorization": f"Bearer {token}"})
        return r.json()

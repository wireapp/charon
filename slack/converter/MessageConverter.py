# {
#    "headers":{
#       "User-Agent":"Python/3.7.6 slackclient/2.5.0 Darwin/19.3.0",
#       "Content-Type":"application/json;charset=utf-8",
#       "Authorization":"Bearer <token>"
#    },
#    "data":"None",
#    "files":"None",
#    "params":"None",
#    "json":{
# {'username': 'Echo Bot', 'icon_emoji': ':robot_face:', 'text': 'You said: hello bot', 'channel': 'GV04GUC82'}#    }
# }
import logging

from common.Config import Config
from roman.RomanClient import RomanClient
from services.TokenDatabase import BotRegistration


class NewMessage:
    def __init__(self, config: Config):
        self.config = config

    def process_bot_message(self, bearer: str, json: dict):
        bot = BotRegistration.get_bot_by_bearer(bearer)
        token = bot.conversations[json['channel']]
        msg = self.to_roman_message(json)
        self.send_msg(msg, token)

    def send_msg(self, msg: dict, token: str):
        logging.info(f'Sending message: {msg}')
        response = RomanClient(self.config).send_message(token, msg)
        logging.info(f'Response: {response}')

    @staticmethod
    def to_roman_message(json: dict) -> dict:
        return {
            'type': 'text',
            'text': json['text']
        }

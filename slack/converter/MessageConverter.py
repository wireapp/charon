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

import emoji

from common.Config import Config
from roman.RomanClient import RomanClient
from services.TokenDatabase import BotRegistration


class NewMessage:
    def __init__(self, config: Config):
        self.config = config

    def process_bot_message(self, bearer: str, json: dict):
        bot = BotRegistration.get_bot_by_bearer(bearer)
        token = bot.conversations[json['channel']]
        msg = to_roman_message(json)
        self.send_msg(msg, token)

    def send_msg(self, msg: dict, token: str):
        logging.info(f'Sending message: {msg}')
        response = RomanClient(self.config).send_message(token, msg)
        logging.info(f'Response: {response}')


def to_roman_message(json: dict) -> dict:
    return {
        'type': 'text',
        'text': get_text(json)
    }


def get_text(json: dict) -> str:
    text = process_text(json)
    text = process_bold_text(text)
    text = process_emojis(text)
    return text


def process_text(json: dict) -> str:
    text = json.get('text')
    if text:
        return text
    blocks = json.get('blocks')
    if not blocks:
        logging.error('Wrong message format')
        return 'Slack bot sent unrecognized message.'
    texts = [block['text']['text'] for block in blocks if block['type'] == 'section']
    return "\n".join(texts)


def process_emojis(test: str) -> str:
    return emoji.emojize(test, use_aliases=True)


def process_bold_text(text: str) -> str:
    return text.replace('*', '**')

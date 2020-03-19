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

logger = logging.getLogger(__name__)


class NewMessage:
    def __init__(self, config: Config):
        self.config = config

    def process_bot_message(self, bearer: str, json: dict):
        logger.debug(f'Processing message {json}')

        bot = BotRegistration.get_bot_by_bearer(bearer)
        token = bot.conversations[json['channel']]
        msg = to_roman_message(json)
        self.send_msg(msg, token)

    def send_msg(self, msg: dict, token: str):
        logger.info(f'Sending message: {msg}')
        response = RomanClient(self.config).send_message(token, msg)
        logger.info(f'Response: {response}')


def to_roman_message(json: dict) -> dict:
    return {
        'type': 'text',
        'text': get_text(json)
    }


def get_text(json: dict) -> str:
    logger.info('Parsing text from bot message')
    text = process_text(json)

    logger.info('Reformatting bold text')
    text = process_bold_text(text)

    logger.info('Creating emojis')
    text = process_emojis(text)
    return text


def process_text(json: dict) -> str:
    text = json.get('text')
    if text:
        logger.info('Only text block found')
        return text

    blocks = json.get('blocks')
    if not blocks:
        logger.error(f'Wrong message format - {json}')
        return 'Slack bot sent unrecognized message.'

    logger.info('Processing blocks.')
    logger.debug(f'Blocks: {blocks}')

    texts = [block['text']['text'] for block in blocks if block['type'] == 'section']
    return "\n".join(texts)


def process_emojis(test: str) -> str:
    return emoji.emojize(test, use_aliases=True)


def process_bold_text(text: str) -> str:
    return text.replace('*', '**')  # TODO use that only when there are *some text*

import logging

from common.Config import Config
from common.SlackBot import TwoWayBot
from roman.RomanClient import RomanClient
from roman.converter.NewConversation import convert_conversation
from roman.converter.NewMessage import convert_message
from slack.SlackBotClient import SlackBotClient

logger = logging.getLogger(__name__)


def init_response(json: dict, config: Config, two_way: TwoWayBot):
    conversation = get_conversation_info(config, json['token'])
    converted = convert_conversation(two_way, roman_payload=json, conversation=conversation)

    logger.info('Init converted, sending to slack bot')
    send(two_way, converted)
    logger.info('Init sent.')


def new_text_response(json: dict, config: Config, two_way: TwoWayBot):
    conversation = get_conversation_info(config, json['token'])
    converted = convert_message(two_way, roman_payload=json, conversation=conversation)

    logger.info('Message converted, sending to slack bot')
    send(two_way, converted)
    logger.info('New message sent.')


def send(bot: TwoWayBot, payload: dict):
    SlackBotClient(bot).send(payload)


def get_conversation_info(config: Config, token: str) -> dict:
    logger.info('Obtaining information about conversation.')
    logger.debug(f'Conversation info for token: {token}')

    conversation = RomanClient(config).get_conversation_info(token)
    if conversation.get('message'):
        logger.error(f'It was not possible to reach Roman. {conversation}')
        raise Exception('Roman unreachable.')

    return conversation

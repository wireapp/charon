import logging

from common.Config import Config, get_config
from common.SlackBot import BotsConversation
from roman.RomanClient import RomanClient
from slack.converter.MessageConverter import convert_slack_message

logger = logging.getLogger(__name__)


def handle(conversation: BotsConversation, json: dict):
    """
    Handle message sent by slack bot.
    """
    msg = convert_slack_message(json)
    config = get_config()
    # TODO consider sending this in the thread pool
    send_msg(msg, conversation.roman_token, config)


def send_msg(msg: dict, token: str, config: Config):
    logger.info(f'Sending message: {msg}')
    response = RomanClient(config).send_message(token, msg)
    logger.info(f'Response: {response}')

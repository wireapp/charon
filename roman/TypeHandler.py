from common.Config import Config
from common.Utils import get_configuration
from roman.conversions.NewConversation import NewConversationConverter
from services.TokenDatabase import RomanTokenStorage

from slack.SlackBotClient import SlackBotClient


def handle(json: dict):
    config = get_configuration()
    message_type = json['type']
    try:
        {
            'conversation.bot_request': bot_request,
            'conversation.init': init,
            'conversation.new_text': new_text
        }[message_type](json, config)
    except KeyError:
        # type is different
        # TODO log that
        pass


def bot_request(config: Config, json: dict):
    RomanTokenStorage.storage[json['botId']] = json['token']
    # TODO call bot api


def init(config: Config, json: dict):
    converted = NewConversationConverter(config).new_conversation_created(json)
    SlackBotClient(config).send(converted)


def new_text(config: Config, json: dict):
    pass

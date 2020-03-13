import logging

from common.Config import Config
from roman.converter.NewConversation import NewConversationConverter
from services.TokenDatabase import BotRegistration
from slack.SlackBotClient import SlackBotClient


def handle(config: Config, json: dict):
    """
    Handle message received from the Roman
    """
    message_type = json['type']
    logging.info(f'Handling type {message_type}')
    try:
        {
            'conversation.bot_request': bot_request,
            'conversation.init': init,
            'conversation.new_text': new_text
        }[message_type](config, json)
    except KeyError:
        # type is different
        logging.info(f'Unhandled type: {json["type"]}')
        pass
    except Exception:
        logging.exception(f'Exception occurred during processing the message.')


def bot_request(config: Config, json: dict):
    bot_id = json['botId']
    logging.info(f'Bot request for bot id: {bot_id}')

    bot = BotRegistration.get_bot(bot_id)
    bot.add_conversation(json['conversationId'], json['token'])

    logging.info(f'New conversation: {json["conversationId"]} for bot {bot_id} ')


def init(config: Config, json: dict):
    logging.info('Init received, converting it to slack call.')
    bot = BotRegistration.get_bot(json['botId'])

    converted = NewConversationConverter(config, bot).new_conversation_created(json)

    logging.info('Init converted, sending to slack bot')
    SlackBotClient(bot).send(converted)
    logging.info('Init sent')


def new_text(config: Config, json: dict):
    logging.info('New text message received.')
    pass

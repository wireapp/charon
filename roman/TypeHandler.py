import logging

from common.Config import Config
from roman.converter.NewConversation import NewConversationConverter
from roman.converter.NewMessage import NewMessageConverter
from services.TokenDatabase import BotRegistration
from slack.SlackBotClient import SlackBotClient

logger = logging.getLogger(__name__)


def handle(config: Config, json: dict, auth_header: str):
    """
    Handle message received from the Roman
    """
    message_type = json['type']
    logger.info(f'Handling type {message_type}')
    try:
        {
            'conversation.bot_request': bot_request,
            'conversation.init': init,
            'conversation.new_text': new_text
        }[message_type](config, json, auth_header)
    except KeyError:
        # type is different
        logger.info(f'Unhandled type: {json["type"]}')
        pass
    except Exception as ex:
        print(ex)
        logger.exception(f'Exception occurred during processing the message.')


def bot_request(config: Config, json: dict, bearer: str):
    bot_id = json['botId']
    logging.info(f'Bot request for bot id: {bot_id}')

    # TODO temporary hack
    bot = BotRegistration.get_bot_by_bearer(bearer)
    bot.id = bot_id
    BotRegistration.add_bot(bot)

    bot.add_conversation(json['conversationId'], json['token'])

    logger.info(f'New conversation: {json["conversationId"]} for bot {bot_id} ')


def init(config: Config, json: dict, bearer: str):
    logging.info('Init received, converting it to slack call.')
    bot = BotRegistration.get_bot(json['botId'])

    converted = NewConversationConverter(config, bot).new_conversation_created(json)

    logger.info('Init converted, sending to slack bot')
    SlackBotClient(bot).send(converted)
    print('Init sent')


def new_text(config: Config, json: dict, bearer: str):
    logging.info('New text message received.')

    bot = BotRegistration.get_bot(json['botId'])
    converted = NewMessageConverter(config, bot).new_message_posted(json)
    SlackBotClient(bot).send(converted)
    print('New message sent.')

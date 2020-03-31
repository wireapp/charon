import logging

from common.Config import get_config, Config
from common.SlackBot import TwoWayBot
from roman.RomanClient import RomanClient
from roman.converter.NewConversation import convert_conversation
from roman.converter.NewMessage import convert_message
from services.Repository import get_bot, register_conversation
from slack.SlackBotClient import SlackBotClient

logger = logging.getLogger(__name__)


def handle(json: dict, roman_token: str):
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
        }[message_type](json, roman_token)
    except KeyError:
        # type is different
        logger.info(f'Unhandled type: {message_type}')
    except Exception as ex:
        logger.exception(f'Exception occurred during processing the message.')
        logger.debug(f'Exception details: {ex}')


def bot_request(json: dict, roman_token: str):
    bot_id = json['botId']

    logging.info(f'Bot request for bot id: {bot_id}')

    register_conversation(authentication_code=roman_token, bot_id=bot_id, roman_token=json['token'])
    logger.info(f'New conversation: {json["conversationId"]} for bot {bot_id} ')


def init(json: dict, roman_token: str):
    logging.info('Init received, converting it to slack call.')

    bot = get_bot(roman_token)

    if not isinstance(bot, TwoWayBot):
        logger.info('Conversation registered for webhook only bot.')

        config = get_config()
        url = f'{config.charon_url}/slack/webhook/{bot.bot_api_key}/{json["botId"]}'
        logger.debug(f'URL generated - {url}')

        RomanClient(config).send_text_message(json['token'], f'Webhook generated: `{url}`')
        return

    config = get_config()

    # TODO consider executing this inside thread pool
    conversation = get_conversation_info(config, json['token'])
    converted = convert_conversation(bot, roman_payload=json, conversation=conversation)

    logger.info('Init converted, sending to slack bot')
    send(bot, converted)
    logger.info('Init sent')


def new_text(json: dict, roman_token: str):
    logging.info('New text message received.')

    bot = get_bot(roman_token)
    if not isinstance(bot, TwoWayBot):
        logger.info('Init for webhook only bot, skipping.')
        return

    config = get_config()

    # TODO consider executing this inside thread pool
    conversation = get_conversation_info(config, json['token'])
    converted = convert_message(bot, roman_payload=json, conversation=conversation)

    logger.info('Message converted, sending to slack bot')
    send(bot, converted)
    logger.info('New message sent.')


def send(bot: TwoWayBot, payload: dict):
    SlackBotClient(bot).send(payload)


def get_conversation_info(config: Config, token: str) -> dict:
    logger.info('Obtaining information about conversation')
    logger.debug(f'Conversation info for token: {token}')

    conversation = RomanClient(config).get_conversation_info(token)
    if conversation.get('message'):
        logger.error(f'It was not possible to reach Roman. {conversation}')
        raise Exception('Roman unreachable.')

    return conversation

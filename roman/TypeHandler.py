import logging
import threading

from common.Config import get_config
from roman.Responses import init_response, new_text_response
from roman.RomanClient import RomanClient
from services.Repository import get_bot, register_conversation, delete_conversation

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
            'conversation.new_text': new_text,
            'conversation.bot_removed': bot_removed
        }[message_type](json, roman_token)
    except KeyError:
        # type is different
        logger.info(f'Unhandled type: {message_type}')
    except Exception:
        logger.exception(f'Exception occurred during processing the message. For request with payload: {json}')


def bot_removed(json: dict, _: str):
    conversation = json['botId']
    logger.info(f'Deleting conversation {conversation}')
    delete_conversation(conversation)


def bot_request(json: dict, roman_token: str):
    bot_id = json['botId']

    logging.info(f'Bot request for bot id: {bot_id}')

    register_conversation(authentication_code=roman_token, bot_id=bot_id, roman_token=json['token'])
    logger.info(f'New conversation: {json["conversationId"]} for bot {bot_id}')


def init(json: dict, roman_token: str):
    logging.info('Init received, converting it to slack call.')

    bot, two_way = get_bot(roman_token)
    config = get_config()

    if not two_way:
        logger.info('Conversation registered for webhook only bot.')

        url = f'{config.charon_url}/slack/webhook/{bot.bot_api_key}/{json["botId"]}'
        logger.debug(f'URL generated - {url}')

        RomanClient(config).send_text_message(json['token'], f'Webhook generated: `{url}`')
        return

    threading.Thread(target=init_response, args=(json, config, two_way,)).start()


def new_text(json: dict, roman_token: str):
    logging.info('New text message received.')

    bot, two_way = get_bot(roman_token)
    if not two_way:
        logger.info('This is webhook bot only, ignoring message.')
        return

    config = get_config()
    threading.Thread(target=new_text_response, args=(json, config, two_way,)).start()

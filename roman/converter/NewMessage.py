import logging

from common.SlackBot import TwoWayBot
from common.Utils import generate_timestamp

logger = logging.getLogger(__name__)


def convert_message(bot: TwoWayBot, roman_payload: dict, conversation: dict) -> dict:
    bot_id = roman_payload['botId']

    logger.info(f'Processing message from bot {bot_id}')

    timestamp = generate_timestamp()

    logger.debug(f'Converting message: {roman_payload}')
    return {
        'token': bot.bot_token,
        'team_id': bot_id,  # TODO determine what is in our sense team id, lets assume this is only one team
        'api_app_id': bot_id,
        'event': convert_event(bot_id, timestamp, roman_payload),
        'type': 'event_callback',
        'event_id': roman_payload['messageId'],
        'event_time': timestamp,
        'authed_users': [x['id'] for x in conversation['members']]
    }


def convert_event(bot_id: str, timestamp: int, roman_payload: dict):
    logger.debug('Converting event data.')
    return {
        'client_msg_id': roman_payload['userId'],
        'type': 'message',
        'ts': timestamp,
        'user': roman_payload['userId'],
        'team': roman_payload['botId'],
        'text': roman_payload['text'],
        'channel': bot_id,
        'event_ts': timestamp,
        'channel_type': 'group'  # wire does not support anything else
    }

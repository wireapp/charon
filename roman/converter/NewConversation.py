import logging

from common.SlackBot import TwoWayBot
from common.Utils import generate_timestamp

logger = logging.getLogger(__name__)


def convert_conversation(bot: TwoWayBot, roman_payload: dict, conversation: dict) -> dict:
    bot_id = roman_payload['botId']
    logger.info(f'Converting conversation for bot {bot_id}')
    logger.debug(f'Conversation: {conversation}')

    user = conversation.get('creator') if conversation.get('creator') else conversation['members'][0]['id']
    timestamp = generate_timestamp()

    return {
        'token': bot.bot_token,
        'api_app_id': bot_id,
        'team_id': bot_id,
        # TODO determine what is in our sense team id, lets assume this is only one team
        'event': convert_event(user, timestamp, conversation),
        'type': 'event_callback',
        'event_id': f'{bot_id}:{conversation["id"]}',
        'event_time': timestamp,
        'authed_users': [x['id'] for x in conversation['members']],
    }


def convert_event(user: str, timestamp: int, conversation: dict):
    logger.debug('Converting event')
    return {
        'type': 'message',
        'subtype': 'group_join',
        'ts': timestamp,
        'user': user,
        'text': f'<@{user}> has joined the group',
        'inviter': user,
        'channel': conversation['id'],
        'event_ts': timestamp,
        'channel_type': 'group'  # wire does not support anything else
    }

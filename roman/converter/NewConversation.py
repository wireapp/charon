# SLACK
# {
#    "token":"<token>",
#    "team_id":"TVBTG5W22",
#    "api_app_id":"AUY7PSRNF",
#    "event":{
#       "type":"message",
#       "subtype":"group_join",
#       "ts":"1584043199.000400",
#       "user":"UUWTRSDJ6",
#       "text":"<@UUWTRSDJ6> has joined the group",
#       "inviter":"UUZJW38UR",
#       "channel":"GVB282W1E",
#       "event_ts":"1584043199.000400",
#       "channel_type":"group"
#    },
#    "type":"event_callback",
#    "event_id":"EvUY97PFH8",
#    "event_time":1584043199,
#    "authed_users":[
#       "UUWTRSDJ6"
#    ]
# }

# ROMAN
# {
#     "type": "conversation.init",
#     "botId": "216efc31-d483-4bd6-aec7-4adc2da50ca5",
#     "userId": "4dfc5c70-dcc8-4d9e-82be-a3cbe6661107", // User who originally created this conversation
#     "token": "...",                                   // Use this token to reply to this message - valid for 20 sec
#     "text": "Bot Example Conversation"                // Conversation name
# }

import logging

from common.SlackBot import TwoWayBot
from common.Utils import generate_timestamp

logger = logging.getLogger(__name__)


def convert_conversation(bot: TwoWayBot, roman_payload: dict, conversation: dict) -> dict:
    bot_id = roman_payload['botId']

    logger.info(f'New conversation created for bot {bot_id}')

    logger.debug(f'Conversation: {conversation}')
    # TODO use creator when available
    # user = conversation['creator']
    user = conversation['members'][0]['id']
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
    logger.info('Converting event')
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

# {
#    "token":"<token>",
#    "team_id":"TVBTG5W22",
#    "api_app_id":"AUY7PSRNF",
#    "event":{
#       "client_msg_id":"14982582-8963-4be1-a11e-6fcf529b1944",
#       "type":"message",
#       "text":"hello",
#       "user":"UUZJW38UR",
#       "ts":"1584118619.001100",
#       "team":"TVBTG5W22",
#       "blocks":[
#          {
#             "type":"rich_text",
#             "block_id":"xGIxC",
#             "elements":[
#                {
#                   "type":"rich_text_section",
#                   "elements":[
#                      {
#                         "type":"text",
#                         "text":"hello"
#                      }
#                   ]
#                }
#             ]
#          }
#       ],
#       "channel":"GV04GUC82",
#       "event_ts":"1584118619.001100",
#       "channel_type":"group"
#    },
#    "type":"event_callback",
#    "event_id":"EvV1M76DNF",
#    "event_time":1584118619,
#    "authed_users":[
#       "UUWTRSDJ6"
#    ]
# }

import logging

from common.SlackBot import BotRegistration
from common.Utils import generate_timestamp

logger = logging.getLogger(__name__)


def convert_message(bot: BotRegistration, roman_payload: dict, conversation: dict) -> dict:
    bot_id = roman_payload['botId']

    logger.info(f'Processing message from bot {bot_id}')

    timestamp = generate_timestamp()

    logger.info('Converting message.')
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
    logger.info('Converting event data.')
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

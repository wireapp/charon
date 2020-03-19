import logging

from common.Config import Config, SlackBot
from common.Utils import generate_timestamp
from roman.RomanClient import RomanClient

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

logger = logging.getLogger(__name__)


class NewMessageConverter:
    def __init__(self, config: Config, bot: SlackBot):
        self.client = RomanClient(config)
        self.bot = bot

    def new_message_posted(self, roman_payload: dict) -> dict:
        assert self.bot.id == roman_payload['botId']

        logger.info(f'Processing message from bot {self.bot.id}')
        conversation = self.__get_conversation_info(roman_payload['token'])
        timestamp = generate_timestamp()

        logger.info('Converting message.')
        return {
            'token': self.bot.to_bot_token,
            'team_id': self.bot.id,  # TODO determine what is in our sense team id, lets assume this is only one team
            'api_app_id': self.bot.id,
            'event': self.__convert_event(timestamp, roman_payload, conversation),
            'type': 'event_callback',
            'event_id': roman_payload['messageId'],
            'event_time': timestamp,
            'authed_users': [x['id'] for x in conversation['members']]
        }

    @staticmethod
    def __convert_event(timestamp: int, roman_payload: dict, conversation: dict):
        logger.info('Converting event data.')
        return {
            'client_msg_id': roman_payload['userId'],
            'type': 'message',
            'ts': timestamp,
            'user': roman_payload['userId'],
            'team': roman_payload['botId'],
            'text': roman_payload['text'],
            'channel': conversation['id'],
            'event_ts': timestamp,
            'channel_type': 'group'  # wire does not support anything else
        }

    def __get_conversation_info(self, token: str) -> dict:
        logger.info(f'Obtaining information about conversation')
        logger.debug(f'Using token: {token}')
        return self.client.get_conversation_info(token)

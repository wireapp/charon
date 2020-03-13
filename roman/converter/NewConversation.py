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

from common.Config import Config, SlackBot
from common.Utils import generate_timestamp
from roman.RomanClient import RomanClient


class NewConversationConverter:
    def __init__(self, config: Config, bot: SlackBot):
        self.config = config
        self.bot = bot

    def new_conversation_created(self, roman_payload: dict) -> dict:
        assert self.bot.id == roman_payload['botId']

        conversation = self.__get_conversation_info(roman_payload['token'])

        # TODO use creator when available
        # user = conversation['creator']
        user = conversation['members'][0]['id']
        timestamp = generate_timestamp()

        return {
            'token': self.bot.to_bot_token,
            'api_app_id': self.bot.id,
            'team_id': self.bot.id,  # TODO determine what is in our sense team id, lets assume this is only one team
            'event': self.__convert_event(user, timestamp, conversation),
            'type': 'event_callback',
            'event_id': conversation['id'],
            'event_time': timestamp,
            'authed_users': [x['id'] for x in conversation['members']],
        }

    @staticmethod
    def __convert_event(user: str, timestamp: int, conversation: dict):
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

    def __get_conversation_info(self, token: str) -> dict:
        return RomanClient(self.config).get_conversation_info(token)

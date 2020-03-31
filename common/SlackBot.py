from dataclasses import dataclass


@dataclass
class Bot:
    bot_api_key: str


@dataclass
class TwoWayBot(Bot):
    bot_token: str
    signing_secret: str
    bot_url: str


@dataclass
class BotsConversation:
    bot_api_key: str
    roman_token: str

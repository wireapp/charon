from dataclasses import dataclass


@dataclass
class BotRegistration:
    bot_token: str
    signing_secret: str
    bot_api_key: str
    bot_url: str


@dataclass
class BotsConversation:
    bot_api_key: str
    roman_token: str

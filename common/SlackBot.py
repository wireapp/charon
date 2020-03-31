from dataclasses import dataclass
from typing import Optional


@dataclass
class BotRegistration:
    bot_token: str
    signing_secret: str
    bot_url: str
    # None only during registration request from client
    bot_api_key: Optional[str]
    webhook_only: bool = False


@dataclass
class BotsConversation:
    bot_api_key: str
    roman_token: str

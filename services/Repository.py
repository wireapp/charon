import logging
from dataclasses import asdict
from typing import Optional

from dacite import from_dict

from common.Db import get_db
from common.SlackBot import BotsConversation, Bot, TwoWayBot

logger = logging.getLogger(__name__)


def register_bot(authentication_code: str, bot: Bot):
    """
    Register bot to the system.
    """
    get_db().hmset(f'registration.{authentication_code}', asdict(bot))


def get_bot(authentication_code: str) -> Bot:
    """
    Retrieves bot by auth code.
    """
    data = get_db().hgetall(f'registration.{authentication_code}')
    logger.debug(f'Retrieving: {data}')
    # find out whether this bot has URL, if so it is TwoWayBot
    if data and data.get('bot_url'):
        return from_dict(data_class=TwoWayBot, data=data)

    return from_dict(data_class=Bot, data=data)


def register_conversation(authentication_code: str, bot_id: str, roman_token: str) -> Bot:
    """
    Register new conversation for the authentication_code.
    """
    bot = get_bot(authentication_code)
    payload = BotsConversation(bot_api_key=bot.bot_api_key, roman_token=roman_token)
    data = asdict(payload)
    logger.debug(f'Saving: {data}')
    get_db().hmset(f'conversation.{bot_id}', data)
    return bot


def get_conversation(bot_id: str) -> BotsConversation:
    """
    Retrieves conversation by bot id.
    """
    data = get_db().hgetall(f'conversation.{bot_id}')
    logger.debug(f'Retrieved payload - {data}')
    return BotsConversation(bot_api_key=data['bot_api_key'], roman_token=data['roman_token'])


def get_conversation_checked(bot_id: str, used_api_key: str) -> Optional[BotsConversation]:
    """
    Retrieves conversation and checks token. Returns None if api keys don't match.
    """
    try:
        conversation = get_conversation(bot_id)
        if conversation.bot_api_key == used_api_key:
            return conversation
    except Exception:
        logger.exception('It was not possible to verify the conversation.')

    logger.warning(f'Unverified access for bot {bot_id} and api key {used_api_key} ')
    return None

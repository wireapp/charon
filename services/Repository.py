import logging
from dataclasses import asdict
from typing import Optional, Tuple

from dacite import from_dict

from common.Db import get_db
from common.SlackBot import BotsConversation, Bot, TwoWayBot

logger = logging.getLogger(__name__)


def register_bot(authentication_code: str, bot: Bot):
    """
    Register bot to the system.
    """
    get_db().hmset(f'registration.{authentication_code}', asdict(bot))


def get_bot(authentication_code: str) -> Tuple[Bot, Optional[TwoWayBot]]:
    """
    Retrieves bot by auth code.
    """
    data = get_db().hgetall(f'registration.{authentication_code}')
    # find out whether this bot has URL, if so it is TwoWayBot
    if data and data.get('bot_url'):
        two_way = from_dict(data_class=TwoWayBot, data=data)
        return two_way, two_way

    return from_dict(data_class=Bot, data=data), None


def register_conversation(authentication_code: str, bot_id: str, roman_token: str):
    """
    Register new conversation for the authentication_code.
    """
    bot, _ = get_bot(authentication_code)
    payload = BotsConversation(bot_api_key=bot.bot_api_key, roman_token=roman_token)

    get_db().hmset(f'conversation.{bot_id}', asdict(payload))


def delete_conversation(bot_id: str):
    """
    Deletes conversation.
    """
    count = get_db().delete(f'conversation.{bot_id}')
    logger.info(f'{count} conversation(s) deleted for bot {bot_id}.')


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
        else:
            logger.warning(f'Bot {bot_id} used API key {used_api_key}, but different was expected.')
    except Exception:
        logger.warning(f'It was not possible to obtain conversation! Bot {bot_id} and api key {used_api_key}.')

    return None

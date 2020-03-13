from services.TokenDatabase import BotRegistration


def has_access(bearer: str, channel: str) -> bool:
    try:
        get_roman_token_for_channel(bearer, channel)
        return True
    except Exception:  # TODO probably key value error, need check
        return False


def get_roman_token_for_channel(bearer: str, channel: str) -> str:
    bot = BotRegistration.get_bot_by_bearer(bearer)
    return bot.conversations[channel]

from common.Config import SlackBot


class BotRegistration:
    __storage = {}

    @staticmethod
    def get_bot(bot_id: str) -> SlackBot:
        return BotRegistration.__storage[bot_id]

    @staticmethod
    def add_bot(bot: SlackBot):
        BotRegistration.__storage[bot.id] = bot

    @staticmethod
    def get_bot_by_bearer(token: str) -> SlackBot:
        res = [bot_id for bot_id in BotRegistration.__storage
               if BotRegistration.get_bot(bot_id).to_proxy_token == token]

        return res[0]

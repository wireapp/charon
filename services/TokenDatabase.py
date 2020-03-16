import os

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
        res = [BotRegistration.get_bot(bot_id) for bot_id in BotRegistration.__storage
               if BotRegistration.get_bot(bot_id).to_proxy_token == token]

        return res[0]

    @staticmethod
    def load_from_env():
        id = os.environ.get('BOT_ID')
        if not id:
            return
        try:
            bot = SlackBot(
                id=str(id),
                url=os.environ['BOT_URL'],
                signing_secret=os.environ['SLACK_SIGNING_SECRET'],
                to_bot_token=os.environ['BOT_TOKEN'],
                to_proxy_token=os.environ['SLACK_BOT_TOKEN']
            )
            BotRegistration.add_bot(bot)
        except Exception as ex:
            print(ex)

import logging
import os

from common.SlackBot import SlackBot

logger = logging.getLogger(__name__)


class BotRegistration:
    __storage = {}

    @staticmethod
    def get_bot(bot_id: str) -> SlackBot:
        logger.info(f'Getting bot: {bot_id}')
        return BotRegistration.__storage[bot_id]

    @staticmethod
    def add_bot(bot: SlackBot):
        logger.info(f'Adding bot: {bot.id}')
        BotRegistration.__storage[bot.id] = bot

    @staticmethod
    def get_bot_by_bearer(token: str) -> SlackBot:
        res = [BotRegistration.get_bot(bot_id) for bot_id in BotRegistration.__storage
               if BotRegistration.get_bot(bot_id).to_proxy_token == token]
        logger.info(f'Getting bot by bearer: {token} -> bots found: {len(res)}')
        return res[0]

    @staticmethod
    def load_from_env():
        logger.info('Loading bot from env.')
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
            logger.info('Bot loaded')
            BotRegistration.add_bot(bot)
        except Exception as ex:
            logger.exception(ex)

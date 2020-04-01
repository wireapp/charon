import redis
from flask import current_app as app, g
from redis import Redis

from common.Config import Config, get_config
from common.Utils import get_or_set


def get_db() -> Redis:
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    config = get_config()
    return get_or_set('db', lambda: connect_db(config))


@app.teardown_appcontext
def teardown_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()


def connect_db(config: Config) -> Redis:
    return redis.Redis(host=config.redis_url, port=config.redis_port, charset="utf-8", decode_responses=True)

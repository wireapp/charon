from services.TokenDatabase import RomanTokenStorage


def handle(json: dict):
    message_type = json['type']
    try:
        {
            'conversation.bot_request': bot_request,
            'conversation.init': init,
            'conversation.new_text': new_text
        }[message_type](json)
    except KeyError:
        # type is different
        # TODO log that
        pass


def bot_request(json: dict):
    RomanTokenStorage.storage[json['botId']] = json['token']
    # TODO call bot api


def init(json: dict):
    # TODO maybe handle this? Is this necessary?
    pass


def new_text(json: dict):
    pass

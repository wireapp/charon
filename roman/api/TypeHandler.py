def handle(json: dict):
    message_type = json['type']
    return {
        'conversation.bot_request': bot_request,
        'conversation.init': init,
        'conversation.new_text': new_text
    }[message_type](json)


def bot_request(json: dict):
    pass


def init(json: dict):
    pass


def new_text(json: dict):
    pass

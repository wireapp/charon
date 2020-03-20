# {
#    "headers":{
#       "User-Agent":"Python/3.7.6 slackclient/2.5.0 Darwin/19.3.0",
#       "Content-Type":"application/json;charset=utf-8",
#       "Authorization":"Bearer <token>"
#    },
#    "data":"None",
#    "files":"None",
#    "params":"None",
#    "json":{
# {'username': 'Echo Bot', 'icon_emoji': ':robot_face:', 'text': 'You said: hello bot', 'channel': 'GV04GUC82'}#    }
# }
import logging

import emoji

logger = logging.getLogger(__name__)


def convert_slack_message(json: dict) -> dict:
    """
    Convert slack message to Roman message.
    """
    return {
        'type': 'text',
        'text': get_text(json)
    }


def get_text(json: dict) -> dict:
    """
    Process text part of the message.
    """
    logger.info('Parsing text from bot message')
    text = format_text(json)

    logger.info('Reformatting bold text')
    text = process_bold_text(text)

    logger.info('Creating emojis')
    text = process_emojis(text)
    return {
        'data': text,
        'mentions': []
    }


def format_text(json: dict) -> str:
    """
    Formats text in the json payload.
    """
    text = json.get('text')
    if text:
        logger.info('Only text block found')
        return text

    blocks = json.get('blocks')
    if not blocks:
        logger.error(f'Wrong message format - {json}')
        return 'Slack bot sent unrecognized message.'

    logger.info('Processing blocks.')
    logger.debug(f'Blocks: {blocks}')

    texts = [block['text']['text'] for block in blocks if block['type'] == 'section']
    return "\n".join(texts)


def process_emojis(test: str) -> str:
    return emoji.emojize(test, use_aliases=True)


def process_bold_text(text: str) -> str:
    return text.replace('*', '**')  # TODO use that only when there are *some text*

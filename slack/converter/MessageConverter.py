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
import re
from typing import List, Optional

import emoji

logger = logging.getLogger(__name__)


def convert_slack_message(json: dict) -> dict:
    """
    Convert slack message to Roman message.
    """
    return {
        'type': 'text',
        'text': build_wire_text(json)
    }


def build_wire_text(json: dict) -> dict:
    """
    Process text part of the message.
    """
    logger.info('Parsing text from bot message')
    text = parse_text(json)

    logger.info('Converting links to markdown')
    text = process_links(text)

    logger.info('Reformatting text')
    text = transform_formatting(text)

    logger.info('Creating emojis')
    text = process_emojis(text)
    return {
        'data': text
    }


def parse_text(json: dict) -> str:
    """
    Formats text in the json payload.
    """
    text = get_text(json.get('text'))
    blocks = get_blocks(json.get('blocks'))
    attachments = get_attachments(json.get('attachments'))
    return f'{text}\n{blocks}\n{attachments}'


def get_text(txt: Optional[str]) -> str:
    if not txt:
        logger.info('No text found')
        return ''

    logger.info('Text found')
    logger.debug(f'Text: {txt}')
    return txt if txt else ''


def get_blocks(blocks: Optional[List[dict]]) -> str:
    if not blocks:
        logger.info('No blocks found')
        return ''

    logger.info('Processing blocks.')
    logger.debug(f'Blocks: {blocks}')

    texts = [block['text']['text'] for block in blocks if block['type'] == 'section']
    return "\n".join(texts)


def get_attachments(attachments: Optional[dict]) -> str:
    if not attachments:
        logger.info('No attachments found')
        return ''

    logger.info('Attachments found')
    logger.debug(f'Attachments: {attachments}')

    return attachments.get('fields')


def get_fields(fields: Optional[List[dict]]) -> str:
    if not fields:
        logger.info('No fields found')
        return ''

    logger.info('Fields found')
    logger.debug(f'Fields: {fields}')

    data = [f'_{field["title"]}:_' + ' ' if field['short'] else '\n' + field['value'] for field in fields]
    return '\n'.join(data)


def process_links(text: str) -> str:
    def create_link(matchobj) -> str:
        match = matchobj.group(1)
        try:
            url, link = match.split('|')
            return f'[{link}]({url})'
        except Exception:
            logger.warning('It was not possible to split text in URL for link, ignoring.')
        return match

    return re.sub('<(.+?)>', create_link, text)


def process_emojis(text: str) -> str:
    return emoji.emojize(text, use_aliases=True)


def transform_formatting(text: str) -> str:
    def bold_fix(matchobj):
        match = matchobj.group(1)
        return f'**{match}**'

    def italic_fix(matchobj):
        match = matchobj.group(1)
        return f'*{match}*'

    bold_fixed = re.sub(r'\*(.+?)\*', bold_fix, text)
    italic_fixed = re.sub(r'_(.+?)_', italic_fix, bold_fixed)
    return italic_fixed

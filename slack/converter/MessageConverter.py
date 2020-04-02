import logging

from slack.converter.Attachments import get_attachments
from slack.converter.Body import get_text, get_blocks
from slack.converter.TextFormatting import process_links, process_emojis, transform_formatting

logger = logging.getLogger(__name__)


def convert_slack_message(json: dict) -> dict:
    """
    Convert slack message to Roman message.

    >>> convert_slack_message({'text': 'hello world'})
    {'type': 'text', 'text': {'data': 'hello world'}}
    """
    logger.debug(f'Parsing message:\n{json}')
    return {
        'type': 'text',
        'text': build_wire_text(json)
    }


def build_wire_text(json: dict) -> dict:
    """
    Process text part of the message.

    >>> build_wire_text({'text': 'hello world'})
    {'data': 'hello world'}

    >>> build_wire_text({'text': '_hello_ *world* <link|name>'})
    {'data': '*hello* **world** [name](link)'}
    """
    logger.debug('Parsing text from bot message')
    text = parse_text(json)

    logger.debug('Converting links to markdown')
    text = process_links(text)

    logger.debug('Creating emojis')
    text = process_emojis(text)

    logger.debug('Reformatting text')
    text = transform_formatting(text)
    return {
        'data': text
    }


def parse_text(json: dict) -> str:
    """
    Formats text in the json payload.

    >>> text = 'first-line'
    >>> blocks = [{'type': 'section', 'text': {'text':'super-text'}}]
    >>> attachments = [{'color': 'good', 'author_name': 'Lukas', 'fields': [{'title': 'title', 'value': 'value'}]}]
    >>> parse_text({'text': text, 'blocks': blocks, 'attachments': attachments})
    'first-line\\nsuper-text\\n🟢——\\n**Lukas:**\\n`title:`\\nvalue\\n———'
    """
    data = [
        get_text(json.get('text')),
        get_blocks(json.get('blocks')),
        get_attachments(json.get('attachments'))
    ]
    return '\n'.join([part.strip() for part in data if part])

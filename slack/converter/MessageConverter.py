import logging

from slack.converter.Attachments import get_attachments
from slack.converter.Body import get_text, get_blocks
from slack.converter.TextFormatting import process_links, process_emojis, transform_formatting

logger = logging.getLogger(__name__)


def convert_slack_message(json: dict) -> dict:
    """
    Convert slack message to Roman message.
    """
    logger.debug(f'Parsing message:\n{json}')
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

    logger.info('Creating emojis')
    text = process_emojis(text)

    logger.info('Reformatting text')
    text = transform_formatting(text)
    return {
        'data': text
    }


def parse_text(json: dict) -> str:
    """
    Formats text in the json payload.
    """
    data = [
        get_text(json.get('text')),
        get_blocks(json.get('blocks')),
        get_attachments(json.get('attachments'))
    ]
    return '\n'.join([part.strip() for part in data if part])

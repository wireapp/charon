import logging
from typing import Optional, List

logger = logging.getLogger(__name__)


def get_text(txt: Optional[str]) -> str:
    """
    Process text of the message.

    >>> get_text('text')
    'text'
    """
    if not txt:
        return ''

    logger.debug(f'Text: {txt}')
    return txt


def get_blocks(blocks: Optional[List[dict]]) -> str:
    """
    Process blocks.

    >>> get_blocks([{'type': 'section', 'text': {'text':'super-text'}}])
    'super-text'
    >>> get_blocks([{'type': 'section', 'text': {'text':'first'}}, {'type': 'section', 'text': {'text':'second'}}])
    'first\\nsecond'
    """
    if not blocks:
        return ''

    logger.debug(f'Blocks: {blocks}')

    texts = [block['text']['text'] for block in blocks if block.get('type') == 'section']
    return '\n'.join(texts)

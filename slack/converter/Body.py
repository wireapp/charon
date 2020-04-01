import logging
from typing import Optional, List

logger = logging.getLogger(__name__)


def get_text(txt: Optional[str]) -> str:
    """
    Process text of the message.
    """
    if not txt:
        logger.info('No text found')
        return ''

    logger.info('Text found')
    logger.debug(f'Text: {txt}')
    return txt


def get_blocks(blocks: Optional[List[dict]]) -> str:
    """
    Process blocks.
    """
    if not blocks:
        logger.info('No blocks found')
        return ''

    logger.info('Processing blocks.')
    logger.debug(f'Blocks: {blocks}')

    texts = [block['text']['text'] for block in blocks if block.get('type') == 'section']
    return '\n'.join(texts)
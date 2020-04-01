import logging
from typing import Optional, List

logger = logging.getLogger(__name__)


def get_attachments(attachments: Optional[List[dict]]) -> str:
    """
    Process attachments.
    """
    if not attachments:
        logger.info('No attachments found')
        return ''

    logger.info('Attachments found')
    logger.debug(f'Attachments: {attachments}')

    data = "\n".join([get_attachment(attachment) for attachment in attachments])
    return data


def get_attachment(attachment: dict) -> str:
    """
    Process single attachment.
    """
    data = f'{get_author(attachment)}\n{get_fields(attachment.get("fields"))}'

    color = get_color(attachment.get('color'))
    if color:
        data = f'{color} ' + data.replace('\n', f'\n{color} ')

    return data


def get_color(color: Optional[str]) -> str:
    """
    Parse color
    """
    clr = ''
    if color == 'good':
        clr = '🟢'
    elif color == 'danger':
        clr = '🔴'
    return clr


def get_author(attachments: dict) -> str:
    """
    Obtains author of the post.
    """
    author = attachments.get('author')
    link = attachments.get('author_link')
    if not author:
        return ''

    return f'[{author}]({link}) says:' if link else f'*{author}* says:'


def get_fields(fields: Optional[List[dict]]) -> str:
    """
    Fields of the attachment.
    """
    if not fields:
        logger.info('No fields found')
        return ''

    logger.info('Fields found')
    logger.debug(f'Fields: {fields}')

    data = [f'_{field["title"]}:_' + (' ' if field.get('short') else '\n') + field['value'] for field in fields]
    return '\n'.join(data)

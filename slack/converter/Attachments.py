import logging
from typing import Optional, List

logger = logging.getLogger(__name__)


def get_attachments(attachments: Optional[List[dict]]) -> str:
    """
    Process attachments.
    >>> get_attachments([{'color': 'good', 'author_name': 'Lukas', 'fields': [{'title': 'title', 'value': 'value'}]}])
    '🟢——\\n**Lukas:**\\n`title:`\\nvalue\\n———'
    """
    if not attachments:
        return ''

    logger.debug(f'Attachments: {attachments}')

    data = '\n'.join([get_attachment(attachment) for attachment in attachments])
    return data + '\n———'


def get_attachment(attachment: dict) -> str:
    """
    Process single attachment.

    >>> get_attachment({'color': 'good', 'author_name': 'Lukas', 'fields': [{'title': 'title', 'value': 'value'}]})
    '🟢——\\n**Lukas:**\\n`title:`\\nvalue'
    """
    data = get_author(attachment) + get_fields(attachment.get("fields"))
    # choose color
    color = get_color(attachment.get('color'))
    if not color:
        color = '—'
    # prepend and append color
    return f'{color}——\n{data}'


def get_color(color: Optional[str]) -> str:
    """
    Parse color

    >>> get_color('good')
    '🟢'

    >>> get_color('danger')
    '🚨'
    """
    clr = ''
    if color == 'good':
        clr = '🟢'
    elif color == 'danger':
        clr = '🚨'
    elif color:
        logger.info(f'Unknown color: {clr}')

    logger.debug(f'Color: {clr}')
    return clr


def get_author(attachment: dict) -> str:
    """
    Obtains author of the post.

    >>> get_author({'author_name': 'Lukas'})
    '**Lukas:**\\n'

    >>> get_author({'author_name': 'Lukas', 'author_link': 'link'})
    '[Lukas](link):\\n'
    """
    author = attachment.get('author_name')
    link = attachment.get('author_link')
    if not author:
        return ''

    logger.debug(f'Author: {author}')

    return (f'[{author}]({link}):' if link else f'**{author}:**') + '\n'


def get_fields(fields: Optional[List[dict]]) -> str:
    """
    Fields of the attachment.

    >>> get_fields([{'title': 'title', 'short': True, 'value': 'value'}])
    '`title:` value'

    >>> get_fields([{'title': 'title', 'value': 'value'}])
    '`title:`\\nvalue'
    """
    if not fields:
        return ''

    logger.debug(f'Fields: {fields}')

    data = [f'`{field["title"]}:`' + (' ' if field.get('short') else '\n') + field['value'] for field in fields]
    return '\n'.join(data)

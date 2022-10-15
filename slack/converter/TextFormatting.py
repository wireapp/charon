import logging
import re

import emoji

logger = logging.getLogger(__name__)


def process_links(text: str) -> str:
    """
    Converts Slack links to markdown links.

    >>> process_links('something <link|name> else')
    'something [name](link) else'
    >>> process_links('something<not link>else')
    'something not link else'
    """

    def create_link(matchobj) -> str:
        match = matchobj.group(1)
        try:
            url, link = match.split('|')
            return f'[{link}]({url})'
        except Exception:
            logger.warning(f'It was not possible to split text "{match}" in URL for link, ignoring.')
            return f' {match} '

    return re.sub('<(.+?)>', create_link, text)


def process_emojis(text: str) -> str:
    """
    Converts written emojis to the UTF emojis.
    >>> process_emojis('Hello :red_heart:')
    'Hello ❤️'
    """
    return emoji.emojize(text, language='alias')


def transform_formatting(text: str) -> str:
    """
    Fixes bold and italic text.

    >>> transform_formatting('_italic_ *bold* nothing')
    '*italic* **bold** nothing'
    """

    def bold_fix(matchobj):
        match = matchobj.group(1)
        return f'**{match}**'

    def italic_fix(matchobj):
        match = matchobj.group(1)
        return f'*{match}*'

    bold_fixed = re.sub(r'\*(.+?)\*', bold_fix, text)
    italic_fixed = re.sub(r'_(.+?)_', italic_fix, bold_fixed)
    return italic_fixed

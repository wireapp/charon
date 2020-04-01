import logging
import re

import emoji

logger = logging.getLogger(__name__)


def process_links(text: str) -> str:
    """
    Converts Slack links to markdown links.
    """

    def create_link(matchobj) -> str:
        match = matchobj.group(1)
        try:
            url, link = match.split('|')
            return f'[{link}]({url})'
        except Exception:
            logger.warning('It was not possible to split text in URL for link, ignoring.')
            return f' {match} '

    return re.sub('<(.+?)>', create_link, text)


def process_emojis(text: str) -> str:
    """
    Converts written emojis to the UTF emojis.
    """
    return emoji.emojize(text, use_aliases=True)


def transform_formatting(text: str) -> str:
    """
    Fixes bold and italic text.
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

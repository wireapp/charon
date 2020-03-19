import time
from typing import Callable

from flask import g


def generate_timestamp() -> int:
    return int(time.time())


def get_or_set(prop: str, factory: Callable):
    """
    Gets or sets context property.
    """
    if not hasattr(g, prop):
        setattr(g, prop, factory())

    return getattr(g, prop)

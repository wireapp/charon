import time
from typing import Callable

from flask import g, Response


def generate_timestamp() -> int:
    """
    Generates time stamp for the messages.
    """
    return int(time.time())


def get_or_set(prop: str, factory: Callable):
    """
    Gets or sets context property.
    """
    if not hasattr(g, prop):
        setattr(g, prop, factory())

    return getattr(g, prop)


def auth_denied() -> Response:
    """
    Builds 401 response.
    """
    return Response('Access denied, wrong or missing token.', 401)

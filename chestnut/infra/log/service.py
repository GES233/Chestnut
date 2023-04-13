import logging

from ..helpers.utils import is_atty


class ChestnutFormatter(logging.Formatter):
    """Formatter with color."""

    if is_atty():
        ...
    else:
        ...

    def format(self, record: logging.LogRecord) -> str:
        return super().format(record)


logger = logging.getLogger("chestnut.root")
"""logger in Chestnut."""
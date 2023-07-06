import logging
from logging import LogRecord
from typing import Dict

from ..helpers.utils import is_atty


try:
    import colorama

    COLORFUL_TTY = True and is_atty()
except ImportError:
    COLORFUL_TTY = False


if COLORFUL_TTY:
    from colorama import Fore, Back

    levelname_color_config: Dict[str, str] = {
        "DEBUG": Fore.CYAN + "DEBUG" + Fore.RESET + "    ",
        "INFO": Fore.GREEN + "INFO" + Fore.RESET + "     ",
        "WARNING": Fore.YELLOW + "WARNING" + Fore.RESET + "  ",
        "ERROR": Fore.GREEN + "ERROR" + Fore.RESET + "    ",
        "CRITICAL": Back.RED + "CRITICAL" + Back.RESET + " ",
    }


class ChestnutFormatter(logging.Formatter):
    """Formatter with color."""

    def format(self, record: logging.LogRecord) -> str:
        if COLORFUL_TTY:
            record.levelname = levelname_color_config[record.levelname]

        return super().format(record)

    def formatTime(self, record: LogRecord, datefmt: str | None = None) -> str:
        if COLORFUL_TTY and datefmt:
            datefmt = Fore.BLUE + datefmt + Fore.RESET

        return super().formatTime(record, datefmt)


chestnut_logger = logging.getLogger("chestnut.root")
"""logger in Chestnut."""

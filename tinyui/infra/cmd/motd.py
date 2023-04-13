"""To replace Sanic's native MOTD."""
import os, sys
# from shutil import get_terminal_size
import sanic
from typing import Any, Dict, Tuple


# sanic.compat
def is_atty() -> bool:
    return bool(sys.stdout and sys.stdout.isatty())


class TinyMOTD:
    """"""

    icon: str | None
    mode: str
    server_location: str
    version: Dict[str, str | Tuple[int]]
    extra: Dict[str, Any] | None

    def __init__(
        self,
        *,
        icon: str | None,
        mode: str,
        server_location: str,
        versions: Dict[str, Any] = {},
        **extra
    ) -> None:
        if icon:
            self.icon = icon
        self.mode = mode
        self.server_location = server_location
        self.version = dict(sanic=sanic.__version__, **versions)
        self.extra = extra

    def display(self) -> None:
        ...

    @classmethod
    def show(cls, *args, **kwds) -> None:
        class_ = cls(*args, **kwds)
        class_.display()


class SimpleMOTD(TinyMOTD):
    def display(self) -> None:
        ...

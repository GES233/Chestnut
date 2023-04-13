"""To replace Sanic's native MOTD."""
import os, sys
from datetime import datetime, date
from shutil import get_terminal_size
from abc import ABC, abstractmethod
import sanic
from typing import Any, Dict, Tuple

from ..helpers.config.app import AppConfig
from ..helpers.utils import is_atty


CHESTNUT_ICON = """
╔═╗┬ ┬┌─┐┌─┐┌┬┐┌┐┌┬ ┬┌┬┐
║  ├─┤├┤ └─┐ │ ││││ │ │ 
╚═╝┴ ┴└─┘└─┘ ┴ ┘└┘└─┘ ┴  

       🌰🥥🍩🍈
"""


NAIVE_LOGO = """
   ▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄
   █      █▄▄█      █
   █▄▄▄▄▄▄█  █▄▄▄▄▄▄█
          ▄  ▄

 keep simple, keep naive

"""


class TinyMOTD(ABC):
    """"""

    icon: str | None
    mode: str
    current: date | datetime
    server_location: str
    app_config: AppConfig
    version: Dict[str, str | Tuple[int]]
    system_info: Dict[str, str | Tuple[int]]
    extra: Dict[str, Any] | None

    def __init__(
        self,
        *,
        icon: str | None,
        mode: str,
        server_location: str,
        app_config: AppConfig,
        version: Dict[str, Any] = {},
        # TODO: Load prerequisite here.
        chestnut: bool = False,
        naive: bool = False,
        **extra
    ) -> None:
        if chestnut == True and naive == True:
            raise AttributeError

        if naive:
            self.icon = NAIVE_LOGO
        elif chestnut:
            self.icon = CHESTNUT_ICON
        else:
            if icon:
                self.icon = icon

        self.mode = mode
        self.current = datetime.now()
        self.server_location = server_location
        self.app_config = app_config
        self.version = dict(sanic=sanic.__version__, **version)
        self.system_info = dict(platform=sys.platform, version=sys.version)
        self.extra = extra

    @abstractmethod
    def display(self) -> None:
        raise NotImplementedError

    @classmethod
    def show(cls, *args, **kwds) -> None:
        class_ = SimpleMOTD(*args, **kwds) if is_atty() else cls(*args, **kwds)
        class_.display()


class SimpleMOTD(TinyMOTD):
    def display(self) -> None:
        # TODO:
        # [LOGO or ICON]
        # [Welcome]
        # <versions>
        #   <system and device info>
        #   <python versions>
        #   <dependent items>
        #     - framework...
        #     - front-end settings...
        # <information in AppConfig(loaded from instance)>
        ...


class ColorfulMOTD(TinyMOTD):
    def display(self) -> None:
        ...

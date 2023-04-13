"""To replace Sanic's native MOTD."""
import os, sys
from datetime import datetime, date
from shutil import get_terminal_size
from abc import ABC, abstractmethod
import sanic
from typing import Any, Dict, Tuple

from ..helpers.config.app import AppConfig
from ..helpers.logo import sizecalc
from ..helpers.utils import is_atty
from ...__version__ import __version__ as chestnut_version


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
        chestnut: bool = True,
        naive: bool = False,
        **extra
    ) -> None:
        if chestnut == True and naive == True:
            raise AttributeError

        if naive:
            from ..helpers.logo import ICON_NAIVE

            self.icon = ICON_NAIVE
        elif chestnut:
            # Default.
            from ..helpers.logo import CHESTNUT_ICON_MIDIAN

            self.icon = CHESTNUT_ICON_MIDIAN
        else:
            if icon:
                self.icon = icon

        self.mode = mode
        self.current = datetime.now()
        self.server_location = server_location
        self.app_config = app_config
        self.version = dict(
            chestnut=chestnut_version, sanic=sanic.__version__, **version
        )
        self.system_info = dict(platform=sys.platform, version=sys.version)
        self.extra = extra

    @abstractmethod
    def display(self) -> None:
        raise NotImplementedError

    @classmethod
    def show(cls, *args, **kwds) -> None:
        class_ = SimpleMOTD(*args, **kwds) if not is_atty() else cls(*args, **kwds)
        class_.display()


class SimpleMOTD(TinyMOTD):
    def __init__(
        self,
        *,
        icon: str | None,
        mode: str,
        server_location: str,
        app_config: AppConfig,
        version: Dict[str, Any] = {},
        chestnut: bool = False,
        naive: bool = False,
        **extra
    ) -> None:
        super().__init__(
            icon=icon,
            mode=mode,
            serverlocation=server_location,
            app_config=app_config,
            version=version,
            chestnut=chestnut,
            naive=naive,
            **extra
        )
        # TODO: Update icon with size.

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

    def _parse_values(self) -> Dict[str, Any]:
        ...

"""To replace Sanic's native MOTD."""
import os, sys
from datetime import datetime, date
from shutil import get_terminal_size
from abc import ABC, abstractmethod
import sanic
from typing import Any, Dict, Tuple

from ..helpers.config.app import AppConfig
from ..helpers.device import getdiskstatus, PYTHON_VERSION, PLATFORM
from ..helpers.logo import sizecalc
from ..helpers.utils import is_atty
from ...__version__ import __version__ as chestnut_version


class ChestnutMOTD(ABC):
    """"""

    icon: str | None
    """ICON or LOGO of application."""
    mode: str
    """mode of application."""
    current: date | datetime
    server_location: str
    app_config: AppConfig
    version: Dict[str, str | Tuple]
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
        **extra,
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
        python_version = (
            str(PYTHON_VERSION.major)
            + "."
            + str(PYTHON_VERSION.minor)
            + "."
            + str(PYTHON_VERSION.micro)
        )
        self.version = dict(
            python=python_version,
            chestnut=chestnut_version,
            sanic=sanic.__version__,
            **version,
        )
        platform, sys_version, machine = PLATFORM
        self.system_info = dict(platform=platform, version=sys_version, machine=machine)
        self.extra = extra

    @abstractmethod
    def construct(self) -> str:
        raise NotImplementedError

    def display(self, as_string: bool = False) -> str | None:
        content = self.construct()
        if as_string:
            return content
        else:
            # TODO: Replace with log.
            print(content)

    @classmethod
    def show(cls, *args, **kwds) -> None:
        class_ = SimpleMOTD(*args, **kwds) if not is_atty() else cls(*args, **kwds)
        class_.display()

    @classmethod
    def show_test(cls, *args, **kwds) -> str | None:
        class_ = SimpleMOTD(*args, **kwds) if not is_atty() else cls(*args, **kwds)
        return class_.display(as_string=True)


class SimpleMOTD(ChestnutMOTD):
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
        **extra,
    ) -> None:
        super().__init__(
            icon=icon,
            mode=mode,
            server_location=server_location,
            app_config=app_config,
            version=version,
            chestnut=chestnut,
            naive=naive,
            **extra,
        )
        # TODO: Update icon with size.

    def construct(self) -> str:
        bar = "========================"
        content = "" + bar
        # [LOGO or ICON]
        content += (self.icon + bar + "\n") if self.icon is not None else ""
        # [Welcome]
        content += f"Welcome to chestnut(v{self.version['chestnut']})\n"
        # Server info.
        content += f"at {self.server_location}!"
        # Enter
        content += "\n\n"
        # <versions>
        content += "[info]\n"
        #   <system and device info>
        version_align = "  "
        content += (
            version_align
            + f"System: {self.system_info['platform']} {self.system_info['version']}({self.system_info['machine']})\n"
        )
        #   <python versions>
        content += version_align + f"Python  {str(self.version['python'])}\n"
        #   <dependent items>
        #     - framework...
        content += version_align * 2 + f"Sanic v{self.version['sanic']}\n"
        #     - front-end settings...
        #       TODO: Add dependent item:
        #         Nodejs,
        #         Tailwindcss(from Phoenix framework's wrap),
        #         AppRun...
        # <information in AppConfig(loaded from instance)>
        content += "\n[app]\n"
        #   <name>
        #   TODO: present in middle.
        content += version_align + f"Name: `{self.app_config.name}`\n"
        #    <intro>
        if self.app_config.introduction and self.app_config.introduction != "":
            content += self.app_config.introduction + "\n"
        ...
        return content


class ColorfulMOTD(ChestnutMOTD):
    def _parse_values(self) -> Dict[str, Any]:
        ...

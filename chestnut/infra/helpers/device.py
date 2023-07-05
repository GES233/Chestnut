""" `chestnut.infra.device`

    Provice some infomations about the device.
"""
import sys
import shutil
import platform
from pathlib import Path
from typing import Any, Callable, Tuple, Type
from collections import namedtuple


PYTHON_VERSION = sys.version_info
PLATFORM: Tuple[str, str, str] = (
    platform.uname().system,
    platform.uname().version,
    platform.uname().machine,
)
"""(system_name, system_version, machine)"""


def getdisk(path: Path) -> str:
    return path.drive


diskStatus: Callable[[str], Type[Tuple]] = lambda name: namedtuple(
    "Disk_" + name.strip(":"), ["total", "used", "free"]
)


def getdiskstatus(path: Path, convert_: int = 0) -> Tuple[Any, ...]:
    disk = getdisk(path)

    total, used, free = shutil.disk_usage(disk)
    disk = diskStatus(disk)
    return disk(*map(lambda item: item / (1024**convert_), (total, used, free)))


## TODO: Add CPU, GPU, etc.

""" `tinyui.infra.device`

    Provice some infomations about the device.
"""
import sys
import shutil
from pathlib import Path
from typing import Tuple, Any
from collections import namedtuple


PYTHON_VERSION = sys.version_info
PLATFORM = sys.platform


def getdisk(path: Path) -> str:
    return path.drive


diskStatus = lambda name: namedtuple(
    "Disk_" + name.strip(":"), ["total", "used", "free"]
)


def getdiskstatus(path: Path, convert_: int = 0) -> Tuple[Any, ...]:
    disk = getdisk(path)

    total, used, free = shutil.disk_usage(disk)
    disk = diskStatus(disk)
    return disk(*map(lambda item: item / (1024**convert_), (total, used, free)))

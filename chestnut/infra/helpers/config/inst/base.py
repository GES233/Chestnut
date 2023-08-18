from os import environ, PathLike
from pathlib import Path
from typing import Any, Dict

from ...path import INSTANCE_PATH as DEFAULT_INSTANCE_PATH

try:
    import tomllib  # type: ignore
except ImportError:
    import tomli as tomllib  # type: ignore


def setinstance(
    relative_file_path: str,
    file_content: str,
    root_path: PathLike | None = None,
    overwrite: bool = True,
) -> None:
    config_path = _parsemultidir(relative_file_path, root_path, True)

    if not config_path.exists():
        config_path.touch()

    if overwrite:
        config_path.write_text(data=file_content, encoding="utf-8")


def loadinstance(
    relative_file_path: str,
    root_path: PathLike | None = None
) -> Dict[str, Any]:
    path = _parsemultidir(relative_file_path, root_path)

    if not path.exists():
        raise FileNotFoundError

    return tomllib.loads(path.read_text("utf-8"))


def loadappconfig(
    relative_file_path: str,
    root_path: PathLike | None = None
) -> Dict[str, Any]:
    whole = loadinstance(relative_file_path, root_path)

    return whole["app"]


def loaddepsconfig(
    relative_file_path: str,
    root_path: PathLike | None = None
) -> Dict[str, dict]:
    whole = loadinstance(relative_file_path, root_path)

    return whole["deps"]


def _parsemultidir(
    relative_file_path: str,
    root_path: PathLike | None = None,
    create_if_not_exist: bool = False,
) -> Path:
    root_path = _getrootpath(root_path)

    if "/" in relative_file_path or "\\" in relative_file_path:
        path_segment = (
            relative_file_path.split("/")
            if ("/" in relative_file_path)
            else relative_file_path.split("\\")
        )
        path_segment.pop()

        _path = root_path
        for _dir in path_segment:
            _path = _path / _dir
            if not _path.exists():
                _path.mkdir()
    
    if create_if_not_exist:
        (root_path / relative_file_path).touch()
    
    return root_path / relative_file_path


def _getrootpath(
    root_path: PathLike | None = None, envvar_instance: str = "STARW_INSTANCE_PATH"
) -> Path:
    if not root_path:
        root_path = Path(
            environ.get(envvar_instance, DEFAULT_INSTANCE_PATH)
        )

    if not isinstance(root_path, Path):
        root_path = Path(root_path)

    return root_path


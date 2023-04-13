from pathlib import Path
from typing import Any, Dict

try:
    import tomllib  # type: ignore
except ImportError:
    import tomli as tomllib  # type: ignore


def setinstance(path: Path | str, content: str) -> None:
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        path.touch()

    path.write_text(content, "utf-8")


def loadinstance(path: Path | str) -> Dict[str, Any]:
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise FileNotFoundError

    return tomllib.loads(path.read_text("utf-8"))


def loadappconfig(path: Path | str) -> Dict[str, Any]:
    whole = loadinstance(path)

    return whole["app"]


def loaddepsconfig(path: Path | str) -> Dict[str, dict]:
    whole = loadinstance(path)

    return whole["deps"]

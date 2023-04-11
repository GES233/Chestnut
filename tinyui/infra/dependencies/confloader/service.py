from typing import Iterable, Dict, Any

from ...helpers.config.dependency import DepsConfig


def _config_validation(config: DepsConfig, assert_items: Iterable[str]) -> None:
    assert config.name in ["confloader"]

    for item in assert_items:
        assert item in config.values


def confpathfromconfig(config: DepsConfig) -> Any:
    _config_validation(config, [])

    ...


class ConfLoader:
    ...

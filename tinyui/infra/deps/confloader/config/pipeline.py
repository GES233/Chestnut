from typing import Any, Callable, Dict
from enum import Enum


language: Callable[[dict | str, str | None], str] = (
    lambda content, lang: content if not isinstance(content, dict) else content[lang]
)


class PipelineConfig:
    """"""

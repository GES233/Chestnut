from typing import Any, Dict
from enum import Enum


language = (
    lambda content, lang: content if not isinstance(content, dict) else content[lang]
)


class PipelineConfig:
    """"""

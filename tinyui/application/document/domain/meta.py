from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from ...base.domain.value_object import ValueObject


@dataclass
class DocumentMeta(ValueObject):
    """Present meta infomation of file(always extract from it)."""

    name: str
    title: str | None
    language: str
    source: Path
    """The path of the raw document."""
    location: str
    """How to locate the document object in application."""
    categories: Iterable[str | None]

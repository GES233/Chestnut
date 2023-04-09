from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from ...base.domain.entity import Entity
from ...base.domain.value_object import ValueObject


@dataclass
class Document:
    """Present a ... to WebPage in disk."""

    name: str
    title: str | None
    source: Path
    """The path of the raw document."""
    location: Iterable[str | None]
    """How to locate the document object in application."""
    categories: Iterable[str | None]
    content: str | None


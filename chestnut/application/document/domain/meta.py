from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from ...core.domain.value_object import ValueObject


@dataclass
class DocumentMeta(ValueObject):
    """Present meta infomation of file(always extract from it)."""

    name: str
    title: str | None
    language: str
    source: Path
    """The path of the raw document."""
    location: Iterable[str]
    """How to locate the document object in application, e.g.`/aaa/bbb/cc`"""
    categories: Iterable[str | None]
    repo_name: str = "main"

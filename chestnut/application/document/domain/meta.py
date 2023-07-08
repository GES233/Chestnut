from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

from ...core.domain.value_object import ValueObject


@dataclass
class DocumentMeta(ValueObject):
    """Present meta infomation of file(always extract from it)."""

    name: str
    title: str | None
    language: str
    source: Path | None
    """The path of the raw document."""
    location: Iterable[str]
    """
    How to locate the document object in application.

    `/aaa/bbb/cc` => ['aaa', 'bbb', 'cc'].
    """
    categories: Iterable[str | None]
    repo_name: str = "main"
    # Compat with database.
    change_time: datetime | None = datetime.utcnow()

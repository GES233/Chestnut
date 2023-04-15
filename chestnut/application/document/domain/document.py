from dataclasses import dataclass
from typing import Any, Dict

from .meta import DocumentMeta
from ...core.domain.entity import AggregateRoot, Entity


@dataclass
class Document(AggregateRoot):
    """Present a markdown file into DomainObject."""

    id: str
    meta: DocumentMeta
    content: str | None

    # SQLAlchemy mapper args.
    __mapper_args__ = dict()


class ParsedDocument(Entity):
    """"""


class ContentUpdateService:
    """Replace document link to route(relative)."""

    def toentity(self) -> Document:
        ...

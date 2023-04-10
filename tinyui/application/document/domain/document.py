from dataclasses import dataclass

from .meta import DocumentMeta
from ...base.domain.entity import AggregateRoot


@dataclass
class Document(AggregateRoot):
    """Present a markdown file into DomainObject."""

    id: str
    meta: DocumentMeta
    content: str | None

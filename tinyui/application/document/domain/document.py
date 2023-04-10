from dataclasses import dataclass

from .meta import DocumentMeta
from ...base.domain.entity import AggregateRoot


@dataclass
class Document(AggregateRoot):
    """Present a markdown file into DomainObject."""

    id: str
    meta: DocumentMeta
    content: str | None

    # SQLAlchemy mapper args.
    __mapper_args__ = dict()


class ContentUpdateService:
    """Replace document link to route(relative)."""

    def toentity(self) -> Document:
        ...

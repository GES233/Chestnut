import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Tuple, List, Callable, Type

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

    @classmethod
    def load(cls, meta: DocumentMeta, content: str) -> "Document":
        return Document(id=meta.name, meta=meta, content=content)

    @classmethod
    def onlymeta(cls, meta: DocumentMeta) -> "Document":
        return Document(id=meta.name, meta=meta, content="")


Section = Dict[str, Tuple[int, str | Type["Section"] | Iterable[str | Type["Section"]]]]
"""{header name: (header level, content/sub paragraph)}"""


class ParsedDocument(Entity):
    """"""

    id: str  # Query by MAIN title.
    """In ParsedDocument, `id` refers `title`."""
    index: Iterable[str]  # except title.
    content:Iterable[Section]


class MarkdownContentSplitService:
    """Split content."""

    HEADER_PATTERN = re.compile(
        r"^(#+ .*)\n",  # Only one group.
        re.MULTILINE,
    )
    getheaderlength: Callable[[str], int] = lambda header: len(header.split(" ")[0])
    """Return the number of `'#'` in header."""

    @staticmethod
    def getheaderbody(header: str) -> str:
        header.split(" ").remove(header.split(" ")[0])
        return " ".join(header)

    @staticmethod
    def parse(content: str, strategy: Any) -> ParsedDocument | None:
        content_chain = re.split(MarkdownContentSplitService.HEADER_PATTERN, content)

        # Remove "\n".
        if not content_chain[0].startswith("#"):
            content_chain.pop(0)

        paragraph_chain: List[Section] = []

        if paragraph_num := len(content_chain) % 2 == 0:
            # Last one in content.
            paragraph_num = int(paragraph_num / 2)
        else:
            # Last one is header.
            content_chain.append("")
            paragraph_num = int((paragraph_num + 1) / 2)

        # Build.
        for idx in range(paragraph_num):
            # header, content
            #   ||      ||
            #   2x,    2x+1(may out of index)
            paragraph_chain.append(
                {
                    MarkdownContentSplitService.getheaderbody(content_chain[idx * 2]): (
                        MarkdownContentSplitService.getheaderlength(content_chain[idx * 2]),
                        content_chain[idx * 2 + 1],
                    )
                }
            )
        
        # Orgnize.
        section_chain: Iterable[Section] = []

        for section in paragraph_chain:
            ...

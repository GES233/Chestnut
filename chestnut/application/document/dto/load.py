import re
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Any, Iterable, Callable

from .. import exception as doc_exc
from ..domain.meta import DocumentMeta
from ..domain.document import Document
from ...core.dto.io import InputSchemaMixin
from ...core.dto.db import DataAccessObjectMixin


# TODO: Replace as `DAOMixin`
class DocumentLoader(InputSchemaMixin, BaseModel):
    content: str
    # Same as DocumentMeta.
    name: str
    title: str | None
    language: str
    source: Path
    location: Iterable[str]
    categories: List[str | None]

    @classmethod
    def fromdict(
        cls,
        input_dict: dict,
        read_service: Callable[[str | Path], str],
        parse_service: Callable[..., dict],
    ) -> "DocumentLoader":
        """`file_path` and `root_path` required."""

        # input_dict: ["file_path"], ["root_path"]
        content = read_service(input_dict["file_path"])

        return DocumentLoader(
            content=content,
            **parse_service(
                content=content,
                file_path=input_dict["file_path"],
                root_path=input_dict["root_path"],
            ),
        )

    def toentity(self) -> Document:
        return DocumentLoader.sqeeze(
            content=self.content,
            meta_dict=dict(
                name=self.name,
                title=self.title,
                language=self.language,
                source=self.source,
                location=self.location,
                categories=self.categories,
            ),
        )

    @staticmethod
    def sqeezetometa(meta_dict: dict) -> DocumentMeta:
        return DocumentMeta(
            name=meta_dict["name"],
            title=meta_dict.get("title", None),
            language=meta_dict["language"],
            source=meta_dict["source"],
            location=meta_dict["location"],
            categories=meta_dict["categories"],
        )

    @staticmethod
    def sqeeze(content: str, meta_dict: dict) -> Document:
        meta = DocumentLoader.sqeezetometa(meta_dict=meta_dict)
        return Document(file_id=meta.name, meta=meta, content=content)

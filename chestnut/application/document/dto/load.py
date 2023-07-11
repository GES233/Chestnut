import re
from datetime import datetime
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
    meta: DocumentMeta
    """This is too useful to use it at this layer."""

    @classmethod
    def fromdict(
        cls,
        input_dict: dict,
        read_service: Callable[[str | Path], str] | None,
        parse_service: Callable[..., dict],
    ) -> "DocumentLoader":
        """
        if load from path, `file_path` and `root_path` in input_dict are required;

        else, `assets_path` and `content` is required.
        """

        if "file_path" in input_dict:
            # FilePathAdapter

            assert read_service

            content = read_service(input_dict["file_path"])
            meta = DocumentLoader.sqeezetometa(
                parse_service(
                    content=content,
                    file_path=input_dict["file_path"],
                    root_path=input_dict["root_path"],
                )
            )

            return DocumentLoader(content=content, meta=meta)
        else:
            # MetadataParserAdapter

            assert "content" in input_dict

            meta = DocumentLoader.sqeezetometa(
                parse_service(
                    content=input_dict["content"],
                    assets_path=input_dict["assets_path"],
                )
            )

            return DocumentLoader(
                content=input_dict["content"],
                meta=meta,
            )

    def toentity(self) -> Document:
        return DocumentLoader.sqeeze(
            content=self.content,
            meta_dict=dict(
                name=self.meta.name,
                title=self.meta.title,
                language=self.meta.language,
                source=self.meta.source,
                location=self.meta.location,
                categories=self.meta.categories,
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
            create_time=meta_dict.get("create_time", datetime.utcnow()),
            change_time=meta_dict.get("change_time", datetime.utcnow()),
        )

    @staticmethod
    def sqeeze(content: str, meta_dict: dict) -> Document:
        meta = DocumentLoader.sqeezetometa(meta_dict=meta_dict)
        return Document(file_id=meta.name, meta=meta, content=content)

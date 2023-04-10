from pathlib import Path
from pydantic import BaseModel
from typing import Iterable

from .. import exception as doc_exc
from ..domain.meta import DocumentMeta
from ..domain.document import Document
from ...base.dto.io import OutputSchemaMixin


class DocumentPresenter(OutputSchemaMixin, BaseModel):
    content: str
    name: str
    title: str
    language: str
    source: str | Path
    location: str
    categories: Iterable[str | None]
    content_enable: bool
    """Different by Usecase. In only meta required, it is `False`."""

    @classmethod
    def fromentity(
        cls, entity: Document, has_content: bool = True
    ) -> "DocumentPresenter":
        if isinstance(entity, Document):
            return DocumentPresenter(
                **DocumentPresenter.parse(document=entity)
            )
        raise TypeError

    @staticmethod
    def parse(document: Document, has_content: bool = True) -> dict:
        return dict(
            content=document.content,
            name=document.meta.name,
            title=document.meta.title,
            language=document.meta.language,
            source=document.meta.source,
            location=document.meta.location,
            categories=document.meta.categories,
            content_enable=has_content,
        )

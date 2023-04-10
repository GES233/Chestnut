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

    @classmethod
    def fromentity(cls, entity: Document | DocumentMeta) -> "DocumentPresenter":
        if isinstance(entity, Document):
            return DocumentPresenter(**DocumentPresenter.parse(document=entity))
        elif isinstance(entity, DocumentMeta):
            document_entity = Document(id=entity.name, meta=entity, content="")
            return DocumentPresenter(
                **DocumentPresenter.parse(document=document_entity)
            )
        raise doc_exc.DomainModelTypeInvalid

    @staticmethod
    def parse(document: Document) -> dict:
        return dict(
            content=document.content,
            name=document.meta.name,
            title=document.meta.title,
            language=document.meta.language,
            source=document.meta.source,
            location=document.meta.location,
            categories=document.meta.categories,
        )

from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, Field, validator
from typing import Iterable, Callable, Optional

from .. import exception as doc_exc
from ..domain.meta import DocumentMeta
from ..domain.document import Document
from ...core.dto.io import OutputSchemaMixin


class DocumentPresenter(OutputSchemaMixin, BaseModel):
    content: str
    name: str
    title: str
    language: str
    source: str | Path = ""
    location: Iterable[str]
    categories: Iterable[str | None]
    create_time: Optional[datetime] = None
    change_time: Optional[datetime] = None

    @validator("create_time", pre=True, always=True)
    def default_create(cls, v: datetime | float):
        if not v:
            return datetime.utcnow()
        else:
            return v if isinstance(v, datetime) else datetime.fromtimestamp(v)

    @validator("change_time", pre=True, always=True)
    def default_update(cls, v: datetime | float, values: dict):
        return (
            v if isinstance(v, datetime) else datetime.fromtimestamp(v)
        ) or values["change_time"]

    @classmethod
    def fromentity(cls, entity: Document | DocumentMeta) -> "DocumentPresenter":
        if isinstance(entity, Document):
            return DocumentPresenter(**DocumentPresenter.parse(document=entity))
        elif isinstance(entity, DocumentMeta):
            document_entity = Document(file_id=entity.name, meta=entity, content="")
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
            create_time=document.meta.create_time,
            change_time=document.meta.change_time,
        )

    def present(
        self,
        render_service: Callable[[str], str] | None,
        link_process_service: Callable[[str], str] = lambda x: x,
        as_json: bool = False,
    ) -> str:
        content = link_process_service(self.content)
        if as_json:
            return content
        else:
            if render_service:
                return render_service(content)
            else:
                return content

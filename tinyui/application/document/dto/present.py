from pathlib import Path
from pydantic import BaseModel
from typing import Any, Tuple

from .. import exception as doc_exc
from ..domain.meta import DocumentMeta
from ..domain.document import Document
from ...base.dto.io import OutputSchemaMixin


class DocumentPresenter(OutputSchemaMixin, BaseModel):
    document: Document

    @classmethod
    def fromentity(cls, entity: Document) -> "DocumentPresenter":
        if isinstance(entity, Document):
            return DocumentPresenter(document=entity)
        raise TypeError

    def todict(self) -> dict:
        return dict(
            meta=self.document.meta,
            content=self.document.content
        )

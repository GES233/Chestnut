from typing import Any, List

from .. import exception as doc_exc
from ..domain.document import Document
from ..domain.meta import DocumentMeta
from ..domain.repo import DocMetaRepo, DocRepo
from ..dto.present import DocumentPresenter


class DisplayIndex:
    repo: DocMetaRepo

    def __init__(self, repo: DocMetaRepo) -> None:
        self.repo = repo

    async def __call__(self) -> Any:
        return await self.display()

    async def display(self) -> List[DocumentPresenter]:
        meta_list: List[DocumentMeta | None] = await self.repo.display()

        return [
            DocumentPresenter.fromentity(
                Document(file_id=meta_item.name, meta=meta_item, content="")
            )
            for meta_item in meta_list
            if meta_item
        ]


class DisplayDocument:
    repo: DocRepo

    def __init__(self, repo: DocRepo) -> None:
        self.repo = repo

    async def show(self, name: str) -> DocumentPresenter:
        content = await self.repo.loadbyname(name)

        if len(content) == 0:
            raise doc_exc.DocumentNotFound
        else:
            content = content[0]
        if content is None:
            raise doc_exc.DocumentNotFound

        return DocumentPresenter.fromentity(entity=content)

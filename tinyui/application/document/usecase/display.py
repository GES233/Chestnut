from typing import Any, List

from ..domain.document import Document
from ..domain.meta import DocumentMeta
from ..domain.repo import DocMetaRepo
from ..dto.present import DocumentPresenter


class DisplayIndex:
    repo: DocMetaRepo

    def __init__(self, repo: DocMetaRepo) -> None:
        self.repo = repo

    async def __call__(self, *args: Any, **kwds: Any) -> Any:
        return await self.display()

    async def display(self) -> List[DocumentPresenter]:
        meta_list: List[DocumentMeta | None] = await self.repo.display()

        return [
            DocumentPresenter.fromentity(
                Document(id=meta_item.name, meta=meta_item, content="")
            )
            for meta_item in meta_list
            if meta_item
        ]

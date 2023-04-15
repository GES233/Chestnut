from typing import Any, List

from ..domain.document import Document
from ..domain.repo import DocRepo
from ..dto.present import DocumentPresenter
from .. import exception as doc_exc


class DisplayDocument:
    repo: DocRepo

    def __init__(self, repo: DocRepo) -> None:
        self.repo = repo

    async def __call__(self, *args: Any, **kwds: Any) -> Any:
        return await self.show(*args, **kwds)

    async def show(self, name: str) -> DocumentPresenter:
        content = await self.repo.loadbyname(name)

        if len(content) == 0:
            raise doc_exc.DocumentNotFound
        else:
            content = content[0]
        if content is None:
            raise doc_exc.DocumentNotFound

        return DocumentPresenter.fromentity(entity=content)

from typing import Any

from .. import exception as doc_exc
from ..domain.document import Document
from ..domain.meta import DocumentMeta
from ..domain.repo import DocRepo, DocMetaRepo


class BuildIndex:
    repo: DocRepo

    def __init__(self, repo: DocRepo) -> None:
        self.repo = repo

    async def __call__(self, *args: Any, **kwds: Any) -> Any:
        if await self.repo.check():
            # if have => update
            return await self.update()
        else:
            # else => build
            return await self.build()

    async def build(self, *args: Any, **kwds: Any) -> Any:
        pass

    async def update(self, *args: Any, **kwds: Any) -> Any:
        # 1.Check diff
        # 2.Update
        pass

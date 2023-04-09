from abc import ABC, abstractmethod
from typing import List, Any

from .document import Document
from .meta import DocumentMeta


class DocRepo(ABC):
    @abstractmethod
    async def loadbyname(self, name: str) -> List[Document | None]:
        """Load specific document br name."""

        raise NotImplementedError

    @abstractmethod
    async def loadbycondition(self, **condition) -> List[Document | None]:
        """Load some documents by condition(e.g. specific language)."""

        raise NotImplementedError

    @abstractmethod
    async def upgrade(self) -> None:
        """Upgrade document and meta."""

        raise NotImplementedError


class DocMetaRepo(ABC):
    @abstractmethod
    async def display(self) -> List[DocumentMeta | None]:
        """Display ALL existed documents's META(except raw content)."""

        raise NotImplementedError


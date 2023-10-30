from abc import ABC, abstractmethod
from typing import List, Any


class FeedRepo(ABC):
    """Use inner join query."""

    @abstractmethod
    async def totalfeedsnumber(self, author) -> int:
        raise NotImplementedError

    @abstractmethod
    async def presentfromauthor(self, author, range) -> List[Any]:
        raise NotImplementedError

    @abstractmethod
    async def appendfeed(self, author, feed) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def deletefeed(self, feed_id) -> None:
        raise NotImplementedError

    @abstractmethod
    async def presentfeed(self, feed_id) -> Any:
        raise NotImplementedError


class PostRepo(ABC): ...
class ThreadRepo(ABC): ...
class CommentRepo(ABC): ...

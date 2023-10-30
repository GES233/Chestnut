from dataclasses import dataclass
from typing import List, Any

from .base import Content, ContentBody


class FeedBody(ContentBody):
    content: str
    tags: List[str | None]

    def __init__(self, body: str, tags: List[Any] = []) -> None:
        self.content = body
        self.tags = tags


@dataclass
class Feed(Content):
    content: FeedBody

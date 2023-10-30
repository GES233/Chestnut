from dataclasses import dataclass
from typing import List, Any

from ...shared_kernel.content.domain import Content, ContentBody, TagRef


class FeedBody(ContentBody):
    content: str
    tags: List[TagRef]

    def __init__(self, body: str, tags: List[TagRef] = []) -> None:
        self.content = body
        self.tags = tags


@dataclass
class Feed(Content):
    content: FeedBody

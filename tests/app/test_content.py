import pytest

import asyncio
from datetime import datetime
from sqlalchemy import Table
from sqlalchemy.sql import select, update
from sqlalchemy.orm import registry
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection
from typing import Any, Callable, Dict, Coroutine, List

from chestnut.application.shared_kernel.content.domain import Content, Status, TagRef, UserRef
from chestnut.application.content.domain.feed import Feed, FeedBody
from chestnut.application.content.domain.repo import FeedRepo
# from dto


class TestFeedDomain:
    def test_feed_body(self):
        content = "My name's Glenn Quagmire, I like gigitty."
        tags = [TagRef("Family Guys", 5), TagRef("Quagmire", 14)]

        body = FeedBody(body=content,tags=tags)
        # Current version of tag is string.

    def test_feed(self):
        content = "Gigitty, gigitty, gigitty gigitty gigitty."
        body = FeedBody(body=content)

        # Feed
        inner_id = 73256098
        author = UserRef(12, "CXK")

        feed = Feed(
            inner_id=inner_id,
            status=Status.normal,
            author=author,
            content=body,
            create_at=datetime.utcnow()
        )


class TestFeedDTO:
    ...

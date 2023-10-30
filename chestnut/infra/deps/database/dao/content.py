from sqlalchemy import (
    String,
    Text,
    DateTime,
    ForeignKey,
)
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import ChestnutBase


class ContentBaseDAO(ChestnutBase):
    __tablename__ = "content_base"

    index_id: Mapped[int] = mapped_column(unique=True, primary_key=True)
    count_id: Mapped[int] = mapped_column(unique=False, nullable=False, primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(16))
    created_at: Mapped[datetime] = mapped_column(DateTime)

    # author = relationship()


class FeedDAO(ChestnutBase):
    __tablename__ = "feeds"

    feeds_id: Mapped[int] = mapped_column(ForeignKey("content_base.count_id"), primary_key=True)
    content: Mapped[str] = mapped_column(Text)


class ThreadDAO(ChestnutBase):
    __tablename__ = "threads"

    feeds_id: Mapped[int] = mapped_column(ForeignKey("content_base.count_id"), primary_key=True)
    title: Mapped[str] = mapped_column()

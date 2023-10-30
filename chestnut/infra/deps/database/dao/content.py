from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    PrimaryKeyConstraint,
    ForeignKeyConstraint,
    UniqueConstraint,
    Index,
)
from .base import chestnut_sqlite_metadata


content_base_table = Table(
    "content_base",
    chestnut_sqlite_metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("index", Integer),
    Column("author", Integer),
    Column("status", String(16)),
    Column("create_at", DateTime),
    # FK author -> user.id
    ForeignKeyConstraint(["author"], ["users.id"]),
)


feeds_table = Table(
    "feeds",
    chestnut_sqlite_metadata,
    Column("feeds_id", Integer, primary_key=True),
    Column("content", Text),
    ForeignKeyConstraint(["feeds_id"], ["content_base.index"]),
)

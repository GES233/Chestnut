from sqlalchemy import (
    Table,
    Column,
    String,
    DateTime,
    PrimaryKeyConstraint,
    ForeignKeyConstraint,
    UniqueConstraint,
    Index,
)
from .base import tiny_sqlite_metadata


document_repo_table = Table(
    "document_repo",
    tiny_sqlite_metadata,
    Column("name", String, default="main"),
    Column("path", String),
    Column("lang", String),  # Root path.
    PrimaryKeyConstraint("name", "lang", name="document_repo_pk"),
    UniqueConstraint("name", "path"),
    # TODO: Add on_update and on_delete.
)


# This table will deleted if re-update/re-install.
document_table = Table(
    "document",
    tiny_sqlite_metadata,
    Column("name", String),  # Route `a/b` => `a_b`
    Column("repo_name", String, default="main"),
    Column("lang", String, nullable=True),
    Column("path", String),  # Physical path in device.
    Column("title", String, nullable=True),
    Column("content", String),
    Column("change_time", DateTime),
    PrimaryKeyConstraint("name", "repo_name", name="document_pk"),  # Name and language
    ForeignKeyConstraint(
        ["repo_name", "lang"], ["document_repo.name", "document_repo.lang"]
    ),
    UniqueConstraint("name", "title"),
    Index("idx_title", "title"),
    Index("idx_content", "content"),
)
"""Table of raw markdown file with some classification."""

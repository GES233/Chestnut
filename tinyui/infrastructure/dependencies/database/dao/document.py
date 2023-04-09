from sqlalchemy import (
    Table,
    Column,
    String,
    DateTime,
    PrimaryKeyConstraint,
)
from .base import tiny_sqlite_metadata

# This table will deleted if re-update/re-install.
document_table = Table(
    "document",
    tiny_sqlite_metadata,
    Column("name", String),  # Route `a/b` => `a_b`
    Column("lang", String),
    Column("path", String),  # Physical path in device.
    Column("title", String),
    Column("content", String),
    Column("change_time", DateTime),
    PrimaryKeyConstraint("name", "lang", name="document_pk"),  # Name and language
)
"""Table of raw markdown file with some classification."""

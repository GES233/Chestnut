from sqlalchemy import (
    Table,
    Column,
    String,
    DateTime,
    PrimaryKeyConstraint,
)
from .base import tiny_sqlite_metadata

prerequisite_table = Table(
    "prerequisite",
    tiny_sqlite_metadata,
    Column("name", String),
    Column("status", String),
    Column("check_time", DateTime),
    PrimaryKeyConstraint("name", name="prerequisite_pk"),
)

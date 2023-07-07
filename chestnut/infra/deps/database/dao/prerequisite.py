from sqlalchemy import (
    Table,
    Column,
    String,
    DateTime,
    PrimaryKeyConstraint,
)
from .base import chestnut_sqlite_metadata

prerequisite_table = Table(
    "prerequisite",
    chestnut_sqlite_metadata,
    Column("name", String),
    Column("status", String),
    Column("check_time", DateTime),
    PrimaryKeyConstraint("name", name="prerequisite_pk"),
)

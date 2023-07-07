from sqlalchemy import (
    Table,
    Column,
    String,
    UUID,
    DateTime,
    PrimaryKeyConstraint,
)
from .base import chestnut_sqlite_metadata

required_table = Table(
    "required",
    chestnut_sqlite_metadata,
    Column("name", String),
    Column("item_type", String),
    Column("info", String),
    Column("update_time", DateTime),
    PrimaryKeyConstraint("name", name="required_pk"),
)

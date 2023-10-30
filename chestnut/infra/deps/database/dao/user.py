from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    BLOB,
)
from .base import ChestnutBase


class UserDAO(ChestnutBase):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String, index=True)
    email = Column(String, index=True)
    birthday = Column(Date)
    description = Column(Text)
    password = Column(BLOB)
    join_at = Column(DateTime)


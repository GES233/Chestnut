from sqlalchemy import (
    Text,
    Date,
    DateTime,
    BLOB,
)
from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column

from .base import ChestnutBase


class UserDAO(ChestnutBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nickname: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(index=True)
    birthday: Mapped[date] = mapped_column(Date)
    description: Mapped[str] = mapped_column(Text)
    password: Mapped[BLOB] = mapped_column(BLOB)
    join_at: Mapped[datetime] = mapped_column(DateTime)


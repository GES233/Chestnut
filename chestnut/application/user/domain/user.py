from enum import Enum
from datetime import date, datetime
from dataclasses import dataclass
from typing import Any

from ...core.domain import Entity, ValueObject


class Status(str, Enum):
    normal = "normal"
    deleted = "deleted"
    frozen = "frozen"


@dataclass
class User(Entity):
    id: int
    nickname: str
    status: Status
    email: str
    birthday: date | None
    description: str | None
    join_at: datetime


@dataclass
class PasswordForm(ValueObject):
    nickname: str
    email: str
    password: str

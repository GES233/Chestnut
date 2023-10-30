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
    birthday: date
    description: str
    join_at: datetime

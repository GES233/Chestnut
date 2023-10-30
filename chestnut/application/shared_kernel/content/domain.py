from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import NamedTuple, Any

from ...core.domain import Entity, ValueObject as VOMixin


class Status(VOMixin, str, Enum):
    normal = "normal"
    invisible = "invisible"
    deleted = "deleted"
    non_interactive = "non_interactive"

    def visibleforeveryone(self) -> bool:
        return self.value == self.normal or self.value == self.non_interactive

    def visibleforauthor(self) -> bool:
        return (
            self.value == self.normal
            or self.value == self.invisible
            or self.value == self.non_interactive
        )

    def interactive(self) -> bool:
        """include star, comment, like, etc."""

        return self.value == self.normal

    @classmethod
    def fromvalue(cls, value: str) -> Any:
        if isinstance(value, str):
            # value = (value.title(),)
            return cls(value)
        for item in cls:
            if item.value == value:
                return item
        return None


@dataclass
class Content(Entity):
    inner_id: int
    status: Status
    author: "UserRef"
    # UserRef: VO
    content: "ContentBody"
    create_at: datetime

    def __eq__(self, __o: object) -> bool:
        return self.inner_id == __o.inner_id if isinstance(__o, type(self)) else False

    def __hash__(self) -> int:
        return hash(self.inner_id)

    def delete(self):
        self.status = Status.deleted

    def invisible(self):
        self.status = Status.invisible


class ContentBody(VOMixin):
    ...


class UserRef(NamedTuple):
    id: int
    nickname: str


class TagRef(NamedTuple):
    value: str
    id: int

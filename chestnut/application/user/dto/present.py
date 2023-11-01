from pydantic import BaseModel, validator, ValidationError

from ..domain.user import User, Status
from ...shared_kernel.content.domain import UserRef


class UserPresentTable(BaseModel):
    id: int
    nickname: str
    status: str

    @classmethod
    def fromdomain(cls, user: User) -> "UserPresentTable":
        return UserPresentTable(
            id=user.id, nickname=user.nickname, status=user.status.value
        )


class UserProfile(BaseModel):
    """Relavent to domain model."""

    id: int
    nickname: str
    email: str

    @classmethod
    def fromdomain(cls, user: User) -> "UserProfile":
        return UserProfile(
            id=user.id, nickname=user.nickname, email=user.email
        )

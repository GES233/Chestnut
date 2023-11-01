from typing import Any

from ..domain.user import User, Status
from ..dto.present import UserPresentTable, UserProfile, UserRef


class UserPresentUsecase:
    user: User

    def __init__(self, user: User) -> None:
        self.user = user

    def __call__(
        self, adapter_type: type[UserRef | UserProfile | UserPresentTable]
    ) -> Any:
        if (
            adapter_type == type(UserRef)
            or isinstance(adapter_type, UserRef)
        ):
            return UserRef(id=self.user.id, nickname=self.user.nickname)
        else:
            return adapter_type.fromdomain(self.user) # type: ignore

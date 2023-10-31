from typing import Callable

from ..exception import CommonUser
from ..domain.user import PasswordForm, User
from ..domain.repo import UserRepo


class RegisterService:
    repo: UserRepo

    def __init__(self, user: PasswordForm, repo: UserRepo):
        self.user = user
        self.repo = repo

    async def __call__(self) -> User:
        common_user = await self.repo.checkcommonuser(self.user.email)

        if common_user:
            raise CommonUser(conflict_email=self.user.email)

        return await self.repo.add(self.user)


class PasswordService:
    en_func: Callable[[str], bytes]
    de_func: Callable[[str, bytes], bool]

    def __init__(self, en, de) -> None:
        self.en_func = en
        self.de_func = de

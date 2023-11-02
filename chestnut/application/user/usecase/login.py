from typing import Any, Callable

from ..dto.login import LoginForm
from ..domain.user import User
from ..domain.repo import UserRepo
from ..exception import NoUserMatched


class LoginUsecase:

    def __init__(self, repo: UserRepo, password_check_service: Callable[[str, bytes], bool]) -> None:
        self.repo = repo
        self.check_service = password_check_service

    async def __call__(self, dto: LoginForm) -> User:
        user = await self.repo.getbyemail(dto.email)
        if user:
            password = await self.repo.returnpassword(user)
            if self.check_service(dto.password, password):
                return user
        raise NoUserMatched

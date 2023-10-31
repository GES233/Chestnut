from datetime import datetime
from typing import Any, Callable

from ..domain.user import User
from ..domain.token import UserToken, TokenScope
from ..domain.repo import UserRepo, UserTokenRepo


class AppendTokenUsecase:
    repo: UserTokenRepo
    user2session: Callable[..., UserToken]

    def __init__(self, repo: UserTokenRepo, service_user2session: Callable[..., UserToken]) -> None:
        self.repo = repo
        self.user2session = service_user2session
    
    async def __call__(self, user: User) -> UserToken:
        token = self.user2session(user)

        _, token = await self.repo.addtoken(token)

        return token


class RemoveTokenUsecase:
    ...


class CheckTokenUsecase:
    ...

from datetime import datetime
from typing import Any, Callable

from ..domain.user import User
from ..domain.token import UserToken, TokenScope
from ..domain.repo import UserRepo, UserTokenRepo
from ..exception import TokenExpire, TokenInvalid
from ..service.user_auth import givetokenundersession, verifytokenundersession


class AppendTokenUsecase:
    repo: UserTokenRepo
    user2session: Callable[..., UserToken]
    default_scope: TokenScope | None

    def __init__(
        self,
        repo: UserTokenRepo,
        service_user2session: Callable[..., UserToken],
    ) -> None:
        self.repo = repo
        self.user2session = service_user2session

    async def __call__(self, user: User) -> UserToken:
        token = self.user2session(user)

        _, token = await self.repo.addtoken(token)

        return token


class RemoveTokenUsecase:
    repo: UserTokenRepo

    def __init__(self, repo: UserTokenRepo) -> None:
        self.repo = repo

    async def removebyuser(self, user: User) -> None:
        ...


class CheckTokenUsecase:
    repo: UserTokenRepo

    def __init__(self, repo: UserTokenRepo) -> None:
        self.repo = repo

    async def token_to_user(self, token: bytes, scope: TokenScope) -> User:
        return await self.repo.getuserbytokenandscope(token, scope)

    async def token_valid(self, token: bytes, scope: TokenScope) -> bool:
        has_user = await self.token_to_user(token, scope)
        if has_user:
            return True
        else:
            return False

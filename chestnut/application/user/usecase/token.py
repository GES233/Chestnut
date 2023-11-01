from datetime import datetime
from typing import Any, Callable

from ..exception import NoUserMatched, TokenInvalid, TokenExpire
from ..domain.user import User
from ..domain.token import UserToken, TokenScope
from ..domain.repo import UserTokenRepo
from ..dto.present import UserPresentTable


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

    async def removebytoken(self, token: bytes) -> None:
        await self.repo.removetokenbyself(token)

    async def removebyuser(self, user: User) -> None:
        ...

    async def removebyuserandscope(self, user: User, scope: TokenScope) -> None:
        ...


class CheckTokenUsecase:
    repo: UserTokenRepo
    scope: TokenScope

    def __init__(self, repo: UserTokenRepo, default_scope: TokenScope) -> None:
        self.repo = repo
        self.scope = default_scope

    async def token_to_user(self, token: bytes) -> User:
        return await self.repo.getuserbytokenandscope(token, self.scope)

    async def token_valid(self, token: bytes) -> bool:
        try:
            has_user = await self.token_to_user(token)
        except (NoUserMatched, TokenInvalid):
            return False

        if has_user:
            return True
        else:
            return False


class ReturnUserUsecase:
    repo: UserTokenRepo
    scope: TokenScope
    parse_request_service: Callable[..., bytes]

    def __init__(
        self,
        repo: UserTokenRepo,
        current_scope: TokenScope,
        analyse_request: Callable[..., bytes],
    ) -> None:
        self.repo = repo
        self.scope = current_scope
        self.parse_request_service = analyse_request

    async def request_to_user(self, request) -> User | None:
        token = self.parse_request_service(request)

        return await self.repo.getuserbytokenandscope(token, self.scope)

    async def request2user_slience(self, request):
        try:
            user = await self.request_to_user(request)
        except:
            return None
        return user

    @staticmethod
    def domain2dto(user: User) -> UserPresentTable:
        return UserPresentTable.fromdomain(user)


class UpdateTokenUsecase:
    def __init__(self) -> None:
        pass

    async def update(self): ...

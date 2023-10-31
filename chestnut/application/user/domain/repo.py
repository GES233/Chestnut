from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Any

from .user import User, PasswordForm
from .token import UserToken, TokenScope


class UserRepo(ABC):
    @abstractmethod
    async def getbyid(self, id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def getbyemail(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def getbynickname(self, nickname: str) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, user: PasswordForm) -> User:
        """User without id -> user with id"""

        raise NotImplementedError

    @abstractmethod
    async def edit(self, user: User) -> User:
        raise NotImplementedError

    async def checkcommonuser(self, email: str) -> bool:
        return True if await self.getbyemail(email) else False


class UserTokenRepo(ABC):
    @abstractmethod
    async def getuserbytoken(self, token: bytes) -> User:
        raise NotImplementedError

    @abstractmethod
    async def gettokenbyuser(self, user_id: int) -> Dict[str, UserToken]:
        raise NotImplementedError

    @abstractmethod
    async def addtoken(self, session: UserToken) -> Tuple[int, UserToken]:
        """Token with id."""

        raise NotImplementedError

    @abstractmethod
    async def removetoken(self, session_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def removetokenbyuser(self, user_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def removetokenbyuserandscope(self, user_id: int, scope: TokenScope) -> None:
        raise NotImplementedError

    @abstractmethod
    async def updatesametoken(self, user_id: int, scope: TokenScope) -> None:
        raise NotImplementedError

    async def gettokenbyuserandscope(self, user_id: int, scope: TokenScope) -> UserToken | None:
        tokens = await self.gettokenbyuser(user_id=user_id)
        return tokens[scope.value]

    async def getsessionbyuser(self, user_id: int) -> UserToken | None:
        return await self.gettokenbyuserandscope(user_id=user_id, scope=TokenScope.session)

    async def removesessionbyuser(self, user_id: int) -> None:
        return await self.removetokenbyuserandscope(user_id=user_id, scope=TokenScope.session)

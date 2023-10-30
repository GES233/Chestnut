from abc import ABC, abstractmethod
from typing import List, Any

from .user import User, PasswordForm


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

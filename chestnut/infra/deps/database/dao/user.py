from sqlalchemy import (
    Text,
    Date,
    DateTime,
    BLOB,
)
from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column

from .base import ChestnutBase
from .....application.user.domain.user import User, Status, PasswordForm


class UserDAO(ChestnutBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column()
    nickname: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(index=True)
    birthday: Mapped[date] = mapped_column(Date, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    password: Mapped[BLOB] = mapped_column(BLOB)
    join_at: Mapped[datetime] = mapped_column(DateTime)

    def todomain(self) -> User:
        return User(
            id=self.id,
            status=Status(self.status),
            nickname=self.nickname,
            email=self.email,
            birthday=self.birthday,
            description=self.description,
            join_at=self.join_at,
        )

    @classmethod
    def fromdomain(cls, model: User, password: str) -> "UserDAO":
        return UserDAO(
            id=model.id,
            status=model.status.value,
            nickname=model.nickname,
            email=model.email,
            birthday=model.birthday,
            description=model.description,
            password=password,
        )

    @classmethod
    def fromregister(cls, model: PasswordForm) -> "UserDAO":
        return UserDAO(
            nickname=model.nickname, email=model.email, password=model.password
        )


## Impl of interfaces.
from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import List

from .....application.user.domain.repo import UserRepo
from .....application.user.service.register import PasswordService


class defaultUserRepo(UserRepo):
    def __init__(
        self,
        session: AsyncSession,
        dao: UserDAO,
        password_service: PasswordService | None = None,
    ) -> None:
        self.session = session
        self.dao = dao
        self.password_service = password_service

    async def getbyid(self, id: int) -> User | None:
        stmt = select(UserDAO).where(UserDAO.__table__.c.id == id)

        async with self.session.begin():
            user = await self.session.scalars(stmt)
            user = user.one_or_none()

        return user.todomain() if isinstance(user, UserDAO) else None
    
    async def getbyemail(self, email: str) -> User | None:
        stmt = select(UserDAO).where(UserDAO.__table__.c.email == email)

        async with self.session.begin():
            user = await self.session.scalars(stmt)
            user = user.one_or_none()

        return user.todomain() if isinstance(user, UserDAO) else None
    
    async def getbynickname(self, nickname: str) -> List[User]:
        stmt = select(UserDAO).where(UserDAO.nickname == nickname)

        async with self.session.begin():
            users = await self.session.scalars(stmt)
            users = users.all()
        
        if len(users) > 0:
            return list(map(lambda dao: dao.todomain(), users))
        else:
            return []
    
    async def add(self, user: PasswordForm) -> User:
        user_dao = UserDAO.fromregister(user)
        stmt_query =lambda email: select(UserDAO).where(UserDAO.email == email)

        async with self.session.begin():
            self.session.add(user_dao)
            await self.session.commit()
            user_res = await self.session.scalars(stmt_query(user_dao.email))
            user_res = user_res.all()

        return user_res[0].todomain()
    
    async def edit(self, user: User) -> User:
        return await super().edit(user)

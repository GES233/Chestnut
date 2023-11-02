from typing import Dict, Tuple
from sqlalchemy import (
    String,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from datetime import datetime
from sqlalchemy.sql import select, update, and_, or_
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker
from sqlalchemy.orm import relationship, Mapped, mapped_column, Mapper

from chestnut.application.user.domain.user import User

from .base import ChestnutBase
from .user import UserDAO
from .....application.user.exception import NoUserMatched
from .....application.user.domain.token import TokenScope, UserToken
from .....application.user.domain.repo import UserTokenRepo


class UserTokenDAO(ChestnutBase):
    __tablename__ = "user_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[bytes] = mapped_column(unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    scope: Mapped[str] = mapped_column()
    create_at: Mapped[datetime] = mapped_column()
    # Relationship
    # Token -*>--1- User
    # many-to -one
    user = relationship("UserDAO")

    __table_args__ = (UniqueConstraint("user_id", "scope", name="ix_user_tokens"),)

    def todomain(self) -> UserToken:
        return UserToken(
            raw_token=self.token,
            user_id=self.user_id,
            scope=TokenScope.fromvalue(self.scope),  # type: ignore
            create_at=self.create_at,
        )

    @classmethod
    def fromdomain(cls, model: UserToken) -> "UserTokenDAO":
        return UserTokenDAO(
            token=model.raw_token,
            user_id=model.user_id,
            scope=model.scope.value,
            create_at=model.create_at,
        )


class defaultUserTokenRepo(UserTokenRepo):
    def __init__(
        self,
        session: async_sessionmaker[AsyncSession],
    ) -> None:
        self.session = session

    async def getuserbytoken(self, token: bytes) -> User:
        stmt = select(UserDAO).where(
            UserDAO.id
            == (select(UserTokenDAO.user_id).where(UserTokenDAO.token == token))
        )

        async with self.session() as session:
            user_ref = await session.scalars(stmt)
            user = user_ref.one_or_none()

        if not user:
            raise NoUserMatched

        return user.todomain()

    async def getuserbytokenandscope(self, token: bytes, scope: TokenScope) -> User:
        stmt = select(UserDAO).where(UserDAO.id == (
                select(UserTokenDAO.user_id)
                .where(
                    and_(UserTokenDAO.token == token, UserTokenDAO.scope == scope.value)
                ).scalar_subquery()
            )
        )

        async with self.session() as session:
            user_ref = await session.scalars(stmt)
            user = user_ref.one_or_none()

            users = user_ref.all()

        if not user:
            raise NoUserMatched

        return user.todomain()

    async def gettokenbyuser(self, user_id: int) -> Dict[str, UserToken]:
        return await super().gettokenbyuser(user_id)

    async def gettokenbyuserandscope(
        self, user_id: int, scope: TokenScope
    ) -> UserToken | None:
        stmt = select(UserTokenDAO).where(
            and_(UserTokenDAO.user_id == user_id, UserTokenDAO.scope == scope.value)
        )

        async with self.session() as session:
            token = await session.scalars(stmt)
            token = token.one_or_none()

        return token.todomain() if isinstance(token, UserToken) else None

    async def addtoken(self, user_token: UserToken) -> Tuple[int, UserToken]:
        async with self.session() as session:
            # Query before insert.
            stmt_q = select(UserTokenDAO).where(
                and_(
                    UserTokenDAO.user_id == user_token.user_id,
                    UserTokenDAO.scope == user_token.scope.value,
                )
            )
            has_token = await session.scalars(stmt_q)
            has_token = has_token.one_or_none()

            if has_token:
                stmt_update = (
                    update(UserTokenDAO)
                    .where(
                        and_(
                            UserTokenDAO.scope == has_token.scope,  # type: ignore
                            UserTokenDAO.user_id == has_token.user_id,  # type: ignore
                        )
                    )
                    .values(token=user_token.raw_token)
                )
                await session.execute(stmt_update)

            else:
                session.add(UserTokenDAO.fromdomain(user_token))
                await session.commit()

            token = await session.scalars(
                select(UserTokenDAO).where(UserTokenDAO.token == user_token.raw_token)
            )
            token = token.one_or_none()

        return token.id, token.todomain()  # type: ignore

    async def removetoken(self, session_id: int) -> None:
        stmt = (
            update(UserTokenDAO)
            .where(UserTokenDAO.id == session_id)
            .values(scope=TokenScope.nil)
        )

        async with self.session() as session:
            await session.execute(stmt)

    async def removetokenbyself(self, token: bytes) -> None:
        stmt1 = (
            update(UserTokenDAO)
            .where(UserTokenDAO.token == token)
            .values(scope=TokenScope.nil)
        )

        async with self.session() as session:
            await session.execute(stmt1)

    async def removetokenbyuser(self, user_id: int) -> None:
        stmt = (
            update(UserTokenDAO)
            .where(UserTokenDAO.user_id == user_id)
            .values(scope=TokenScope.nil)
        )

        async with self.session() as session:
            await session.execute(stmt)

    async def removetokenbyuserandscope(self, user_id: int, scope: TokenScope) -> None:
        stmt = (
            update(UserTokenDAO)
            .where(
                and_(UserTokenDAO.user_id == user_id, UserTokenDAO.scope == scope.value)
            )
            .values(scope=TokenScope.nil)
        )

        async with self.session() as session:
            await session.execute(stmt)

    async def updatesametoken(self, user_id: int, scope: TokenScope) -> None:
        current = datetime.utcnow()

        stmt = (
            update(UserTokenDAO)
            .where(and_(UserTokenDAO.id == user_id, UserTokenDAO.scope == scope.value))
            .values(create_at=current)
        )
        async with self.session() as session:
            await session.execute(stmt)

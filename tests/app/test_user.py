import pytest

import asyncio
from datetime import datetime
from sqlalchemy.sql import select, update
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection
from typing import Any, Callable, Dict, Coroutine, List

from chestnut.application.user.domain.user import User, PasswordForm, Status
from chestnut.application.user.domain.repo import UserRepo
from chestnut.application.user.dto.register import RegisterForm
from chestnut.application.user.service.register import RegisterService, PasswordService
from chestnut.application.user.usecase.register import RegisterUsecase
from chestnut.infra.deps.database.dao.user import defaultUserRepo, UserDAO


def run_sync(func):
    return asyncio.run(func)


class TestUserDomain:
    ...


class UserRepoTest(UserRepo):
    def __init__(self) -> None:
        self.container_id = {}
        self.container_email = {}
        # {id: {"email": email: "user": UserDAO}}
    
    async def getbyid(self, id: int) -> User | None:
        if len(self.container_id) == 0:
            return None
        return self.container_id[id]
    
    async def getbyemail(self, email: str) -> User | None:
        if len(self.container_email) == 0:
            return None
        return self.container_email[email]
    
    async def add(self, user: PasswordForm) -> User:
        user_dao = UserDAO.fromregister(user)

        id_scalar = len(self.container_id) + 1
        user_dao.id = id_scalar

        return user_dao.todomain()


en = lambda x: f"{x}__"
de = lambda x: x.strip("_")

service = PasswordService(en, de)

class TestRegister:
    def test_service(self):
        ...

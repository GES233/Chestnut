from typing import Any

from ..domain.user import User
from ..domain.repo import UserRepo
from ..dto.register import RegisterForm as Form
from ..service.register import RegisterService as Service


class RegisterUsecase:
    service: Service
    repo: UserRepo
    form: Form

    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo

    async def __call__(self, reg_form: Form) -> User:
        self.service = Service(
            user=reg_form.toentity(),
            repo=self.repo
        )

        return await self.service()

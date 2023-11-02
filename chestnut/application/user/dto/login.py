from pydantic import BaseModel, EmailStr, Field
from typing import Any, Dict

from ...core.dto.io import InputSchemaMixin


class LoginForm(InputSchemaMixin, BaseModel):
    email: EmailStr
    password: str

    @classmethod
    def fromdict(cls, **data) -> "LoginForm":
        return LoginForm(
            email=data.get("email", None), password=data.get("password", None)
        )

    def toentity(self) -> None:
        return None

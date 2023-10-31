from pydantic import BaseModel, EmailStr, Field
from typing import Dict

from ..domain.user import PasswordForm as DomainForm
from ...core.dto.io import InputSchemaMixin


class RegisterForm(BaseModel, InputSchemaMixin):
    nickname: str
    email: EmailStr
    password: str
    remember: bool = Field(default=True)
    # Not related to the 

    @classmethod
    def fromdict(cls, input_dict: Dict) -> "RegisterForm":
        return RegisterForm(
            nickname=input_dict["nickname"],
            email=input_dict["email"],
            password=input_dict["password"]
        )

    def toentity(self):
        return DomainForm(
            nickname=self.nickname,
            email=self.email,
            password=self.password
        )

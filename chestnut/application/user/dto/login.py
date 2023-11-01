from pydantic import BaseModel, EmailStr, Field
from typing import Dict

from ...core.dto.io import InputSchemaMixin


class LoginForm(InputSchemaMixin, BaseModel):
    email: EmailStr
    password: str

import click
from typing import Any

from ..password import pswd_bcrypt_adapter
from ...infra.cmd import manage
from ...infra.deps.database.dao.user import UserDAO, UserRepo
from ...application.user.dto.register import RegisterForm


@manage.group()
def user(): ...


@user.command()
def register():
    """Register from shell."""

    ...


@user.command()
def delete():
    ...

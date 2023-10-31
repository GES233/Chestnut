from sanic.request import Request
from sanic.response import HTTPResponse, redirect
from typing import Any

from ...auth.service import givesessionfromuser, checksession, returnuserfromsession
from ....infra.web.dependency.database import DatabaseDep
from ....infra.deps.database.dao.token import defaultUserTokenRepo


async def loginpresentation(request: Request) -> HTTPResponse:
    ...


async def login(request: Request, dep: DatabaseDep) -> HTTPResponse:
    ...


async def logout(request: Request, dep: DatabaseDep) -> HTTPResponse:
    ...

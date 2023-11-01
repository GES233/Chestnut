from sanic.request import Request
from sanic.response import HTTPResponse, redirect
from typing import Any

from ...auth.service.session import check_session_usecase, append_session_usecase, remove_session_usecase
from ...auth.client.cookie import fetchsession, setsession, releasesession
from ....infra.web.dependency.database import DatabaseDep
from ....infra.deps.database.dao.token import defaultUserTokenRepo


async def loginpresentation(request: Request) -> HTTPResponse:
    ...


async def login(request: Request, dep: DatabaseDep) -> HTTPResponse:
    ...


async def logout(request: Request, dep: DatabaseDep) -> HTTPResponse:
    removesession_serverside = remove_session_usecase(dep.session_maker)

    await removesession_serverside.removebytoken(fetchsession(request))

    # Client side: delete cookie.
    return releasesession(redirect("/"))

from sanic.request import Request
from sanic.response import HTTPResponse, redirect
from typing import Any

from ...auth.service.session import check_session_usecase, append_session_usecase, remove_session_usecase
from ...auth.client.cookie import fetchsession, setsession, releasesession
from ....infra.web.dependency.database import DatabaseDep
from ....infra.deps.database.dao.token import defaultUserTokenRepo
# from ....application.user.usecase import 


async def loginpresentation(request: Request) -> HTTPResponse:
    ...


async def login(request: Request, dep: DatabaseDep) -> HTTPResponse:
    if "current_user" in request.ctx.__dict__:
        return redirect("/")

    # Parse form
    ...

    # Usecase
    try:
        ...
    except:
        # Return form.
        ...
    # Update session.
    getsession_serverside = append_session_usecase(dep.session_maker)

    return redirect("/")


async def logout(request: Request, dep: DatabaseDep) -> HTTPResponse:
    removesession_serverside = remove_session_usecase(dep.session_maker)

    await removesession_serverside.removebytoken(fetchsession(request))

    # Client side: delete cookie.
    return releasesession(redirect("/"))

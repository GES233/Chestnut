from datetime import timedelta
from sanic.request import Request
from sanic.response import HTTPResponse, redirect
from typing import Any

from .form import LoginForm, LoginDTO, validate_login_form, no_user_matched
from ...password import checkpassword
from ...auth.service.session import (
    check_session_usecase,
    append_session_usecase,
    remove_session_usecase,
)
from ...auth.client.cookie import fetchsession, setsession, releasesession
from ....infra.web.blueprints.plain.render import plain_render as render
from ....infra.web.dependency.database import DatabaseDep
from ....infra.deps.database.dao.user import defaultUserRepo
from ....infra.deps.database.dao.token import defaultUserTokenRepo
from ....application.user.usecase.login import LoginUsecase
from ....application.user.exception import NoUserMatched


async def loginpresentation(request: Request) -> HTTPResponse:
    return await render(request, "login.html", context=dict(form=LoginForm()))


async def login(request: Request, dep: DatabaseDep) -> HTTPResponse:
    if "current_user" in request.ctx.__dict__:
        return redirect("/")

    # Parse form
    form_data = request.form
    if not form_data:
        return await render(request, "register.html", context=dict(form=LoginForm()))
    data_lists = {k: form_data.get(k) for k in ["email", "password", "remember"]}
    remember = data_lists["remember"]
    form = LoginForm(data=data_lists)

    model = validate_login_form(form)

    if isinstance(model, LoginForm):
        return await render(request, "login.html", context=dict(form=LoginForm()))

    # Usecase
    service = LoginUsecase(
        repo=defaultUserRepo(dep.session_maker),
        password_check_service=checkpassword,
    )
    try:
        user = await service(model)
    except NoUserMatched:
        # Return form.
        return await render(request, "login.html", context=dict(form=no_user_matched(form)))

    # Update session.
    getsession_serverside = append_session_usecase(dep.session_maker)
    token = await getsession_serverside(user)

    # Add it to cookie.
    return setsession(redirect("/"), token.raw_token, timedelta(days=60))


async def logout(request: Request, dep: DatabaseDep) -> HTTPResponse:
    removesession_serverside = remove_session_usecase(dep.session_maker)

    await removesession_serverside.removebytoken(fetchsession(request))

    # Client side: delete cookie.
    return releasesession(redirect("/"))

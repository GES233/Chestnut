from sanic.request import Request
from sanic.response import HTTPResponse, redirect
from typing import Any

from .form import (
    SignUpForm,
    common_email,
    check_signup_form,
    SignUpModel,
)
from ...password import pswd_bcrypt_adapter
from ....infra.web.blueprints.plain.render import launch_render as render
from ....infra.web.dependency.database import DatabaseDep
from ....infra.helpers.config.app import AppConfig
from ....infra.helpers.config.page import PageConfig
from ....infra.deps.database.dao.user import defaultUserRepo
from ....application.user.exception import CommonUser
from ....application.user.usecase.register import RegisterUsecase


async def registerpresentation(request: Request) -> HTTPResponse:
    request.ctx.page_config.load_items(role="SignUp")

    return await render(request, "register.html", context=dict(form=SignUpForm()))


async def register(request: Request, dep: DatabaseDep) -> HTTPResponse:
    # Check.
    form_data = request.form
    if not form_data:
        return await render(request, "register.html", context=dict(form=SignUpForm()))
    data_lists = {
        k: form_data.get(k)
        for k in ["nickname", "email", "password", "confirm", "remember"]
    }
    remember = data_lists["remember"]
    form = SignUpForm(data=data_lists)
    model = check_signup_form(form)
    if isinstance(model, SignUpForm):
        return await render(request, "register.html", context=dict(form=model))

    # Query.
    service = RegisterUsecase(
        repo=defaultUserRepo(
            session=dep.session_maker, password_service=pswd_bcrypt_adapter
        )
    )
    try:
        user = await service(model)
    except CommonUser:
        # Add modal?
        return await render(request, "register.html", context=dict(form=common_email(form)))

    request.ctx.page_config.load_items()

    # return redirect("/user/register")
    if not remember:
        return redirect("/user/login")
    else:
        # Add auth.
        return await render(request, "register.html", context=dict(form=SignUpForm()))


def formcheck(form):
    ...

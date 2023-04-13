""" `chestnut.adapter.plain.launch`
    ~~~~

    HTML render to plain app.
"""
from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.exceptions import SanicException
from typing import Dict, Any


from ....web.app import EXTENSION_INSTLLED
from ....deps.html.service import returnloaderandenv

if not EXTENSION_INSTLLED:
    from jinja2 import (
        Environment,
        select_autoescape,
        FileSystemLoader,
    )

    from ....helpers.path import TEMPLATE_PATH

    loader, launch_environment = returnloaderandenv(TEMPLATE_PATH, True)

    async def render(
        template_name: str = "",
        status: int = 200,
        headers: Dict[str, str] | None = None,
        content_type: str = "text/html; charset=utf-8",
        app: Sanic | None = None,
        environment: Environment | None = None,
        context: Dict[str, Any] | None = None,
        *,
        template_source: str = "",
    ) -> HTTPResponse:
        environment = environment or launch_environment

        kwargs = context or {}

        if template_name:
            template = environment.get_template(template_name)
        else:
            raise SanicException("Template not found.")

        content = await template.render_async(**kwargs)

        return HTTPResponse(
            body=content,
            status=status,
            headers=headers,
            content_type=content_type,
        )

else:
    from sanic_ext.extensions.templating.render import render


async def launch_render(
    request: Request,
    template_name: str = "",
    status: int = 200,
    headers: Dict[str, str] | None = None,
    content_type: str = "text/html; charset=utf-8",
    context: Dict[str, Any] = {},
) -> HTTPResponse:
    """Only in launched environment."""

    appended_context = context

    # Fetch some content registed on middleware.
    appended_context.update(app_config=request.ctx.app_config)
    appended_context.update(page_config=request.ctx.page_config)

    return await render(
        template_name=template_name,
        status=status,
        headers=headers,
        content_type=content_type,
        app=request.app,  # used when have sanic_ext
        context=appended_context,
        environment=(
            launch_environment
            if not EXTENSION_INSTLLED
            else request.app.ext.environment
        ),
    )

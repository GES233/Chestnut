from sanic import Sanic
from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, redirect

from ....infra.web.blueprints.plain.render import launch_render as render
from ....infra.web.blueprints.plain.path import plain_static
from ....infra.web.settings.location import CONFIG_LOCATION, REQUEST_CONTEXT_LOCATION
from ....infra.web.dependency.database import DatabaseDep
from ....infra.helpers.config.app import AppConfig
from ....infra.helpers.config.page import PageConfig


async def registerpresentation(request: Request) -> HTTPResponse:    
    request.ctx.page_config.load_items()

    return await render(request)


async def register(request: Request, dep: DatabaseDep) -> HTTPResponse:
    
    request.ctx.page_config.load_items()

    return redirect("/")

from sanic import Blueprint
from sanic.request import Request
from sanic.response import file, json, redirect, HTTPResponse
from pathlib import Path

from .paths import webapp_static, WEB_DIR_PATH
from ..plain.web import page_bp as template_bp
from ...exception import custome as custome_exc
from ...settings.location import CONFIG_LOCATION, REQUEST_CONTEXT_LOCATION
from ....helpers.config.app import AppConfig
from ....helpers.config.page import PageConfig


page_bp = Blueprint("page")


@page_bp.route("/heartbeat")
async def heartbeat(request: Request) -> HTTPResponse:
    return json({"di": "da"})


@page_bp.route("/<any>")
async def redir(request: Request, any: str) -> HTTPResponse:
    args = request.query_string

    return redirect("/?{}".format(args) if args else "/")


@page_bp.route("/")
async def catch_all(request: Request) -> HTTPResponse:
    return await file(Path(WEB_DIR_PATH / "index.html"))


# Add middleware for render().
@page_bp.on_request
async def add_info(request: Request) -> None:
    assert CONFIG_LOCATION["app_config"] in request.app.config and isinstance(
        request.app.config[CONFIG_LOCATION["app_config"]], AppConfig
    )

    # AddConfig.
    request.ctx.app_config = request.app.config[CONFIG_LOCATION["app_config"]]
    # PageConfig.
    request.ctx.page_config = PageConfig()


@page_bp.on_response
async def add_mime_type(request: Request, response: HTTPResponse) -> HTTPResponse:
    mime_type = response.content_type

    if mime_type and "charset" not in mime_type:
        mime_type += "; charset=UTF-8"
        response.content_type = mime_type

    return response


web_bp = Blueprint.group(webapp_static, page_bp)
web_bp_without_webapp = Blueprint.group(webapp_static, template_bp)

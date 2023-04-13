""" `chestnut.adapter.plain.index`
    ~~~~

    Return index page of launch application.
"""
from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse

from .render import launch_render as render
from ....helpers.config.page import PageConfig
from ....deps.i18n.language import parse_headers


index_bp = Blueprint("launch_index_bp")


@index_bp.route("/")
async def index(request: Request) -> HTTPResponse:
    # Language.
    language = parse_headers(request.headers)

    # Page Info.
    request.ctx.page_config.load_items(**PageConfig.addtitle(role="Index"))

    # Return.
    return await render(request, "index.html")

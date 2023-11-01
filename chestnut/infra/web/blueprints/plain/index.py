""" `chestnut.adapter.plain.index`
    ~~~~

    Return index page of launch application.
"""
from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse

from .render import plain_render as render
from ....helpers.config.page import PageConfig
from .....adapter.auth.decorators import mountuserfromsession


index_bp = Blueprint("launch_index_bp")


@index_bp.route("/")
@mountuserfromsession
async def index(request: Request) -> HTTPResponse:
    # Language.
    # language = parseheaders(request.headers)

    # Page Info.
    request.ctx.page_config.load_items(**PageConfig.addtitle(role="Index"))

    # Return.
    return await render(request, "launch.html", has_user=True)

""" `chestnut.adapter.plain.web`
    ~~~~

    Application of Chestnut[without node].
"""
from sanic import Sanic
from sanic import Blueprint
from sanic.request import Request

# Using launch blurprints' static service.
from ..path import launch_static
from ....settings.location import CONFIG_LOCATION, REQUEST_CONTEXT_LOCATION
from .....helpers.config.app import AppConfig
from .....helpers.config.page import PageConfig


page_bp = Blueprint("page")
# Import lib here.
# ...


web_plain_bp = Blueprint.group(
    launch_static,
    page_bp,
    # ...
)


def register_plain(app: Sanic) -> None:
    """Register blueprint and add some middleware to Sanic."""

    # Add middleware for render().
    @app.on_request
    async def add_info(request: Request) -> None:
        assert CONFIG_LOCATION["app_config"] in request.app.config and isinstance(
            request.app.config[CONFIG_LOCATION["app_config"]], AppConfig
        )

        # AddConfig.
        request.ctx.app_config = request.app.config[CONFIG_LOCATION["app_config"]]
        # PageConfig.
        request.ctx.page_config = PageConfig()

    # Register blueprint.
    app.blueprint(web_plain_bp)

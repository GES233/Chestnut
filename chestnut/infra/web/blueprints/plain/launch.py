""" `chestnut.adapter.plain.launch`
    ~~~~

    Launch Application of Chestnut.
"""
from sanic import Sanic
from sanic import Blueprint
from sanic.request import Request

from .paths import launch_static
from ...settings.location import CONFIG_LOCATION, REQUEST_CONTEXT_LOCATION
from ....helpers.config.app import AppConfig
from ....helpers.config.page import PageConfig


# Import lib here.
from .index import index_bp

# from .docs import docs_bp


launch_bp = Blueprint.group(launch_static, index_bp)


def register_launch(app: Sanic) -> None:
    """Register launch blueprint and add some middleware to Sanic."""

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
    app.blueprint(launch_bp)

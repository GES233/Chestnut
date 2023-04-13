from sanic import Sanic, Request

from .settings.location import CONFIG_LOCATION
from ..helpers.config.app import AppConfig
from ..helpers.config.page import PageConfig


def register_middleware(app: Sanic):
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

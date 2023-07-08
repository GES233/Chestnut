from sanic import Sanic
from typing import List

from ...log.service import chestnut_logger


def register_blueprint(app: Sanic) -> None:
    """Register all blueprints."""

    from .api import api_bp

    if app.config.APP.build:
        from .web import web_bp as web_bp
    else:
        chestnut_logger.warn("Build not enabled, now use launch-app-like layout.")
        from .web import web_plain_bp as web_bp

    # Web.
    app.blueprint(web_bp)
    app.blueprint(api_bp)


def reload_paths() -> List:
    from .web.path import MAIN_PUBLIC_PATH
    from ...helpers.path import BACKEND_PATH, DOCS_PATH

    return [MAIN_PUBLIC_PATH, BACKEND_PATH, DOCS_PATH]

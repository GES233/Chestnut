from sanic import Sanic
from sanic.log import logger
from typing import List


def register_blueprint(app: Sanic) -> None:
    """Register all blueprints."""

    from .api import api_bp

    if app.config.APP.build:
        from .web import web_bp as web_bp
    else:
        logger.warn("Build not enabled, now use same one as launch app.")
        from .web import web_bp_without_webapp as web_bp

    # Web.
    app.blueprint(web_bp)
    app.blueprint(api_bp)


def reload_paths() -> List:
    from .web.paths import MAIN_PUBLIC_PATH
    from ...helpers.path import BACKEND_PATH, DOCS_PATH

    return [MAIN_PUBLIC_PATH, BACKEND_PATH, DOCS_PATH]

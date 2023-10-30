from sanic import Sanic
from typing import List

from ...log.service import chestnut_logger


def register_blueprint(app: Sanic, from_webapp: bool = False) -> None:
    """Register all blueprints."""

    from .api import api_bp

    from .web.webapp import WEB_DIR_PATH

    if from_webapp and WEB_DIR_PATH.exists():
        from .web import web_bp as web_bp
    else:
        if from_webapp:
            chestnut_logger.warn("Build not enabled, now use template layout.")
        from .web import web_plain_bp as web_bp
        from .plain.web import register_plain

        register_plain(app)

    # Web.
    app.blueprint(web_bp)
    app.blueprint(api_bp)


def reload_paths() -> List:
    from .web.path import MAIN_PUBLIC_PATH
    from ...helpers.path import BACKEND_PATH, DOCS_PATH

    return [MAIN_PUBLIC_PATH, BACKEND_PATH, DOCS_PATH]

from pathlib import Path
from sanic import Blueprint

from ..plain.paths import CSS_PATH, JS_PATH
from ....helpers.path import MAIN_PUBLIC_PATH, ASSETS_PATH


# Configure Paths(it is stable).
WEB_DIR_PATH = Path(MAIN_PUBLIC_PATH / "webapp")

STATIC_PATH = Path(WEB_DIR_PATH / "static")
FONTS_PATH = Path(MAIN_PUBLIC_PATH / "fonts")


webapp_static = Blueprint("web")

# Add static.
# Using-template.
webapp_static.static("/static/css", CSS_PATH, name="web_css")
webapp_static.static("/static/js", JS_PATH, name="web_js")
# Related to front-end.
webapp_static.static("/static", STATIC_PATH, name="static")
webapp_static.static("/assets", ASSETS_PATH, name="assets")
